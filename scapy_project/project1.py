
package main

import (
	"fmt"
	"log"
	"net/http"
	"strings"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/robfig/cron/v3"
	"ipms/config"
	"ipms/internal/db"
	"ipms/internal/handlers"
	"ipms/internal/models"
	"ipms/internal/services"
)

func main() {
	cfg := config.Load()

	database, err := db.New(cfg.DBPath)
	if err != nil {
		log.Fatalf("❌ Database failed: %v", err)
	}

	hub := services.NewHub()
	h   := handlers.New(database, cfg, hub)

	gin.SetMode(gin.ReleaseMode)
	r := gin.New()
	r.Use(gin.Logger(), gin.Recovery())
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:3000", "http://127.0.0.1:3000"},
		AllowMethods:     []string{"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Accept", "Authorization"},
		AllowCredentials: true,
	}))

	// WebSocket
	r.GET("/ws", h.WS)

	api := r.Group("/api")
	api.GET("/health",         h.Health)

	// Core search & analysis
	api.POST("/search",        h.Search)
	api.POST("/analyze",       h.Analyze)
	api.POST("/manual",        h.Manual)
	api.POST("/refresh/:id",   h.Refresh)

	// Profiles
	api.GET("/profiles",            h.ListProfiles)
	api.GET("/profiles/:id",        h.GetProfile)
	api.PATCH("/profiles/:id/risk", h.UpdateRisk)
	api.DELETE("/profiles/:id",     h.DeleteProfile)

	// Reports
	api.GET("/reports",             h.ListReports)
	api.POST("/report/:id",         h.GenerateReport)

	// Dashboard
	api.GET("/stats",               h.Stats)
	api.GET("/chart",               h.Chart)
	api.GET("/activity",            h.Activity)

	// Auto-refresh cron every 10 minutes
	c := cron.New()
	c.AddFunc("*/10 * * * *", func() {
		profiles, err := database.GetAllActive()
		if err != nil || len(profiles) == 0 {
			return
		}
		for _, p := range profiles {
			sp, err := fetchForPlatform(p.Username, p.Platform, cfg)
			if err != nil || sp == nil || sp.NeedsManual {
				continue
			}
			delta := sp.Followers - p.Followers
			risk := services.ScoreRisk(sp, p.Platform)
			database.UpsertProfile(sp, p.Platform, risk.Level, risk.Score)
			database.InsertSnapshot(p.ID, sp.Followers, sp.Following, sp.Posts, delta)
			hub.Broadcast("update", map[string]interface{}{
				"id": p.ID, "username": p.Username,
				"platform": p.Platform, "followers": sp.Followers, "delta": delta,
			})
			if abs64(delta) > 500 {
				sev := "info"
				if abs64(delta) > 5000 { sev = "alert" }
				sign := "+"
				if delta < 0 { sign = "" }
				database.Log(p.Username, p.Platform, "follower_change",
					fmt.Sprintf("Follower change: %s%d for @%s", sign, delta, p.Username), sev)
				hub.Broadcast("alert", map[string]interface{}{
					"username": p.Username, "delta": delta,
				})
			}
		}
		log.Printf("[CRON] Refreshed %d profiles", len(profiles))
	})
	c.Start()

	// Startup banner
	grokS := "❌ Add GROK_API_KEY to .env"
	if cfg.HasGrok() { grokS = "✅ Ready (grok-3-mini)" }
	xS := "❌ Add SOCIALDATA_KEY to .env"
	if cfg.HasSocialData() { xS = "✅ Ready (socialdata.tools)" }
	igS := "⚡ Manual entry"
	if cfg.HasRapidAPI() { igS = "✅ Ready (RapidAPI)" }

	fmt.Println()
	fmt.Println("╔══════════════════════════════════════════════════════════╗")
	fmt.Println("║     IPMS — Intelligent Profile Monitoring System v3.0    ║")
	fmt.Println("║     Muhammad Abdullah Mujahid | 2022-AG-6620 | UAF       ║")
	fmt.Println("╠══════════════════════════════════════════════════════════╣")
	fmt.Printf( "║  🟢 API:       http://localhost:%s/api                ║\n", cfg.Port)
	fmt.Printf( "║  🔌 WebSocket: ws://localhost:%s/ws                   ║\n", cfg.Port)
	fmt.Printf( "║  🤖 Grok AI:   %-42s ║\n", grokS)
	fmt.Printf( "║  𝕏  X/Twitter: %-42s ║\n", xS)
	fmt.Printf( "║  📷 Instagram: %-42s ║\n", igS)
	fmt.Println("║  🐙 GitHub:    ✅ Free API (no key needed)               ║")
	fmt.Println("║  🤖 Reddit:    ✅ Free API (no key needed)               ║")
	fmt.Println("╚══════════════════════════════════════════════════════════╝")
	fmt.Println()

	log.Printf("Server running on :%s", cfg.Port)
	log.Fatal(http.ListenAndServe(":"+cfg.Port, r))
}

func fetchForPlatform(username, platform string, cfg *config.Config) (*models.ScrapedProfile, error) {
	switch strings.ToUpper(platform) {
	case "X":
		return services.FetchX(username, cfg.SocialDataKey)
	case "INSTAGRAM":
		return services.FetchInstagram(username, cfg.RapidAPIKey)
	case "GITHUB":
		return services.FetchGitHub(username)
	case "REDDIT":
		return services.FetchReddit(username)
	default:
		return nil, fmt.Errorf("unknown platform")
	}
}

func abs64(x int64) int64 { if x < 0 { return -x }; return x }