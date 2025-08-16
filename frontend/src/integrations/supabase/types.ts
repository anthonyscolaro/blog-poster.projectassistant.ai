export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  // Allows to automatically instantiate createClient with right options
  // instead of createClient<Database, { PostgrestVersion: 'XX' }>(URL, KEY)
  __InternalSupabase: {
    PostgrestVersion: "13.0.4"
  }
  public: {
    Tables: {
      agent_configs: {
        Row: {
          agent_name: string
          config: Json | null
          created_at: string | null
          custom_prompts: Json | null
          enabled: boolean | null
          id: string
          max_retries: number | null
          max_runs_per_day: number | null
          max_runs_per_hour: number | null
          model_preferences: Json | null
          organization_id: string
          priority: number | null
          retry_delay_seconds: number | null
          timeout_seconds: number | null
          updated_at: string | null
        }
        Insert: {
          agent_name: string
          config?: Json | null
          created_at?: string | null
          custom_prompts?: Json | null
          enabled?: boolean | null
          id?: string
          max_retries?: number | null
          max_runs_per_day?: number | null
          max_runs_per_hour?: number | null
          model_preferences?: Json | null
          organization_id: string
          priority?: number | null
          retry_delay_seconds?: number | null
          timeout_seconds?: number | null
          updated_at?: string | null
        }
        Update: {
          agent_name?: string
          config?: Json | null
          created_at?: string | null
          custom_prompts?: Json | null
          enabled?: boolean | null
          id?: string
          max_retries?: number | null
          max_runs_per_day?: number | null
          max_runs_per_hour?: number | null
          model_preferences?: Json | null
          organization_id?: string
          priority?: number | null
          retry_delay_seconds?: number | null
          timeout_seconds?: number | null
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "agent_configs_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organization_dashboard"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "agent_configs_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organizations"
            referencedColumns: ["id"]
          },
        ]
      }
      articles: {
        Row: {
          canonical_url: string | null
          citations: Json | null
          compliance_flags: string[] | null
          content: string | null
          content_html: string | null
          created_at: string | null
          deleted_at: string | null
          deleted_by: string | null
          excerpt: string | null
          featured_image: string | null
          focus_keyword: string | null
          generation_cost: number | null
          headings_count: number | null
          id: string
          images: string[] | null
          keyword_density: number | null
          keywords: string[] | null
          last_synced_at: string | null
          legal_notes: string | null
          legal_review_status: string | null
          legal_reviewed: boolean | null
          links_external: number | null
          links_internal: number | null
          meta_description: string | null
          meta_title: string | null
          organization_id: string
          previous_versions: Json | null
          published_at: string | null
          readability_score: number | null
          reading_time: number | null
          review_status: string | null
          reviewed_at: string | null
          reviewed_by: string | null
          scheduled_for: string | null
          schema_markup: Json | null
          seo_score: number | null
          shares_count: number | null
          slug: string
          status: string | null
          sync_status: string | null
          title: string
          tokens_used: number | null
          unpublished_at: string | null
          updated_at: string | null
          user_id: string
          version: number | null
          views_count: number | null
          word_count: number | null
          wordpress_id: string | null
          wordpress_site: string | null
          wordpress_url: string | null
        }
        Insert: {
          canonical_url?: string | null
          citations?: Json | null
          compliance_flags?: string[] | null
          content?: string | null
          content_html?: string | null
          created_at?: string | null
          deleted_at?: string | null
          deleted_by?: string | null
          excerpt?: string | null
          featured_image?: string | null
          focus_keyword?: string | null
          generation_cost?: number | null
          headings_count?: number | null
          id?: string
          images?: string[] | null
          keyword_density?: number | null
          keywords?: string[] | null
          last_synced_at?: string | null
          legal_notes?: string | null
          legal_review_status?: string | null
          legal_reviewed?: boolean | null
          links_external?: number | null
          links_internal?: number | null
          meta_description?: string | null
          meta_title?: string | null
          organization_id: string
          previous_versions?: Json | null
          published_at?: string | null
          readability_score?: number | null
          reading_time?: number | null
          review_status?: string | null
          reviewed_at?: string | null
          reviewed_by?: string | null
          scheduled_for?: string | null
          schema_markup?: Json | null
          seo_score?: number | null
          shares_count?: number | null
          slug: string
          status?: string | null
          sync_status?: string | null
          title: string
          tokens_used?: number | null
          unpublished_at?: string | null
          updated_at?: string | null
          user_id: string
          version?: number | null
          views_count?: number | null
          word_count?: number | null
          wordpress_id?: string | null
          wordpress_site?: string | null
          wordpress_url?: string | null
        }
        Update: {
          canonical_url?: string | null
          citations?: Json | null
          compliance_flags?: string[] | null
          content?: string | null
          content_html?: string | null
          created_at?: string | null
          deleted_at?: string | null
          deleted_by?: string | null
          excerpt?: string | null
          featured_image?: string | null
          focus_keyword?: string | null
          generation_cost?: number | null
          headings_count?: number | null
          id?: string
          images?: string[] | null
          keyword_density?: number | null
          keywords?: string[] | null
          last_synced_at?: string | null
          legal_notes?: string | null
          legal_review_status?: string | null
          legal_reviewed?: boolean | null
          links_external?: number | null
          links_internal?: number | null
          meta_description?: string | null
          meta_title?: string | null
          organization_id?: string
          previous_versions?: Json | null
          published_at?: string | null
          readability_score?: number | null
          reading_time?: number | null
          review_status?: string | null
          reviewed_at?: string | null
          reviewed_by?: string | null
          scheduled_for?: string | null
          schema_markup?: Json | null
          seo_score?: number | null
          shares_count?: number | null
          slug?: string
          status?: string | null
          sync_status?: string | null
          title?: string
          tokens_used?: number | null
          unpublished_at?: string | null
          updated_at?: string | null
          user_id?: string
          version?: number | null
          views_count?: number | null
          word_count?: number | null
          wordpress_id?: string | null
          wordpress_site?: string | null
          wordpress_url?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "articles_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organization_dashboard"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "articles_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organizations"
            referencedColumns: ["id"]
          },
        ]
      }
      audit_logs: {
        Row: {
          action: string
          created_at: string | null
          details: Json | null
          id: string
          organization_id: string
          resource_id: string | null
          resource_type: string | null
          user_id: string | null
        }
        Insert: {
          action: string
          created_at?: string | null
          details?: Json | null
          id?: string
          organization_id: string
          resource_id?: string | null
          resource_type?: string | null
          user_id?: string | null
        }
        Update: {
          action?: string
          created_at?: string | null
          details?: Json | null
          id?: string
          organization_id?: string
          resource_id?: string | null
          resource_type?: string | null
          user_id?: string | null
        }
        Relationships: []
      }
      competitors: {
        Row: {
          articles_analyzed: number | null
          articles_found: number | null
          check_frequency: string | null
          created_at: string | null
          domain: string
          enabled: boolean | null
          feed_urls: string[] | null
          id: string
          ignore_keywords: string[] | null
          last_article_date: string | null
          last_checked_at: string | null
          min_word_count: number | null
          name: string
          next_check_at: string | null
          organization_id: string
          sitemap_url: string | null
          track_keywords: string[] | null
          updated_at: string | null
        }
        Insert: {
          articles_analyzed?: number | null
          articles_found?: number | null
          check_frequency?: string | null
          created_at?: string | null
          domain: string
          enabled?: boolean | null
          feed_urls?: string[] | null
          id?: string
          ignore_keywords?: string[] | null
          last_article_date?: string | null
          last_checked_at?: string | null
          min_word_count?: number | null
          name: string
          next_check_at?: string | null
          organization_id: string
          sitemap_url?: string | null
          track_keywords?: string[] | null
          updated_at?: string | null
        }
        Update: {
          articles_analyzed?: number | null
          articles_found?: number | null
          check_frequency?: string | null
          created_at?: string | null
          domain?: string
          enabled?: boolean | null
          feed_urls?: string[] | null
          id?: string
          ignore_keywords?: string[] | null
          last_article_date?: string | null
          last_checked_at?: string | null
          min_word_count?: number | null
          name?: string
          next_check_at?: string | null
          organization_id?: string
          sitemap_url?: string | null
          track_keywords?: string[] | null
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "competitors_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organization_dashboard"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "competitors_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organizations"
            referencedColumns: ["id"]
          },
        ]
      }
      cost_tracking: {
        Row: {
          amount: number
          api_calls: number | null
          article_id: string | null
          billing_cycle: string | null
          billing_month: string | null
          created_at: string | null
          id: string
          organization_id: string
          pipeline_id: string | null
          service: string
          service_detail: string | null
          tokens_input: number | null
          tokens_output: number | null
          tokens_used: number | null
          user_id: string
        }
        Insert: {
          amount: number
          api_calls?: number | null
          article_id?: string | null
          billing_cycle?: string | null
          billing_month?: string | null
          created_at?: string | null
          id?: string
          organization_id: string
          pipeline_id?: string | null
          service: string
          service_detail?: string | null
          tokens_input?: number | null
          tokens_output?: number | null
          tokens_used?: number | null
          user_id: string
        }
        Update: {
          amount?: number
          api_calls?: number | null
          article_id?: string | null
          billing_cycle?: string | null
          billing_month?: string | null
          created_at?: string | null
          id?: string
          organization_id?: string
          pipeline_id?: string | null
          service?: string
          service_detail?: string | null
          tokens_input?: number | null
          tokens_output?: number | null
          tokens_used?: number | null
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "cost_tracking_article_id_fkey"
            columns: ["article_id"]
            isOneToOne: false
            referencedRelation: "article_performance"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "cost_tracking_article_id_fkey"
            columns: ["article_id"]
            isOneToOne: false
            referencedRelation: "articles"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "cost_tracking_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organization_dashboard"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "cost_tracking_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organizations"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "cost_tracking_pipeline_id_fkey"
            columns: ["pipeline_id"]
            isOneToOne: false
            referencedRelation: "pipelines"
            referencedColumns: ["id"]
          },
        ]
      }
      invitations: {
        Row: {
          accepted_at: string | null
          accepted_by: string | null
          created_at: string | null
          email: string
          expires_at: string | null
          id: string
          invited_by: string
          organization_id: string
          role: string
          status: string | null
          token: string
        }
        Insert: {
          accepted_at?: string | null
          accepted_by?: string | null
          created_at?: string | null
          email: string
          expires_at?: string | null
          id?: string
          invited_by: string
          organization_id: string
          role: string
          status?: string | null
          token?: string
        }
        Update: {
          accepted_at?: string | null
          accepted_by?: string | null
          created_at?: string | null
          email?: string
          expires_at?: string | null
          id?: string
          invited_by?: string
          organization_id?: string
          role?: string
          status?: string | null
          token?: string
        }
        Relationships: [
          {
            foreignKeyName: "invitations_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organization_dashboard"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "invitations_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organizations"
            referencedColumns: ["id"]
          },
        ]
      }
      organization_api_keys: {
        Row: {
          allowed_ips: unknown[] | null
          created_at: string | null
          created_by: string | null
          encrypted_key: string
          expires_at: string | null
          id: string
          is_active: boolean | null
          key_hash: string
          key_hint: string | null
          key_name: string
          last_used_at: string | null
          last_used_ip: unknown | null
          organization_id: string
          rate_limit_per_day: number | null
          rate_limit_per_hour: number | null
          revoke_reason: string | null
          revoked_at: string | null
          revoked_by: string | null
          service: string
          updated_at: string | null
          usage_count: number | null
        }
        Insert: {
          allowed_ips?: unknown[] | null
          created_at?: string | null
          created_by?: string | null
          encrypted_key: string
          expires_at?: string | null
          id?: string
          is_active?: boolean | null
          key_hash: string
          key_hint?: string | null
          key_name: string
          last_used_at?: string | null
          last_used_ip?: unknown | null
          organization_id: string
          rate_limit_per_day?: number | null
          rate_limit_per_hour?: number | null
          revoke_reason?: string | null
          revoked_at?: string | null
          revoked_by?: string | null
          service: string
          updated_at?: string | null
          usage_count?: number | null
        }
        Update: {
          allowed_ips?: unknown[] | null
          created_at?: string | null
          created_by?: string | null
          encrypted_key?: string
          expires_at?: string | null
          id?: string
          is_active?: boolean | null
          key_hash?: string
          key_hint?: string | null
          key_name?: string
          last_used_at?: string | null
          last_used_ip?: unknown | null
          organization_id?: string
          rate_limit_per_day?: number | null
          rate_limit_per_hour?: number | null
          revoke_reason?: string | null
          revoked_at?: string | null
          revoked_by?: string | null
          service?: string
          updated_at?: string | null
          usage_count?: number | null
        }
        Relationships: [
          {
            foreignKeyName: "organization_api_keys_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organization_dashboard"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "organization_api_keys_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organizations"
            referencedColumns: ["id"]
          },
        ]
      }
      organizations: {
        Row: {
          articles_limit: number | null
          articles_used: number | null
          billing_cycle_end: string | null
          billing_cycle_start: string | null
          billing_email: string | null
          budget_alert_threshold: number | null
          contact_email: string | null
          created_at: string | null
          current_month_articles: number | null
          current_month_cost: number | null
          deleted_at: string | null
          id: string
          monthly_article_limit: number | null
          monthly_budget: number | null
          name: string
          plan: string | null
          settings: Json | null
          slug: string
          stripe_customer_id: string | null
          stripe_subscription_id: string | null
          subscription_status: string | null
          subscription_tier: string | null
          team_members_limit: number | null
          team_members_used: number | null
          trial_ends_at: string | null
          updated_at: string | null
        }
        Insert: {
          articles_limit?: number | null
          articles_used?: number | null
          billing_cycle_end?: string | null
          billing_cycle_start?: string | null
          billing_email?: string | null
          budget_alert_threshold?: number | null
          contact_email?: string | null
          created_at?: string | null
          current_month_articles?: number | null
          current_month_cost?: number | null
          deleted_at?: string | null
          id?: string
          monthly_article_limit?: number | null
          monthly_budget?: number | null
          name: string
          plan?: string | null
          settings?: Json | null
          slug: string
          stripe_customer_id?: string | null
          stripe_subscription_id?: string | null
          subscription_status?: string | null
          subscription_tier?: string | null
          team_members_limit?: number | null
          team_members_used?: number | null
          trial_ends_at?: string | null
          updated_at?: string | null
        }
        Update: {
          articles_limit?: number | null
          articles_used?: number | null
          billing_cycle_end?: string | null
          billing_cycle_start?: string | null
          billing_email?: string | null
          budget_alert_threshold?: number | null
          contact_email?: string | null
          created_at?: string | null
          current_month_articles?: number | null
          current_month_cost?: number | null
          deleted_at?: string | null
          id?: string
          monthly_article_limit?: number | null
          monthly_budget?: number | null
          name?: string
          plan?: string | null
          settings?: Json | null
          slug?: string
          stripe_customer_id?: string | null
          stripe_subscription_id?: string | null
          subscription_status?: string | null
          subscription_tier?: string | null
          team_members_limit?: number | null
          team_members_used?: number | null
          trial_ends_at?: string | null
          updated_at?: string | null
        }
        Relationships: []
      }
      payment_history: {
        Row: {
          amount: number
          created_at: string
          currency: string | null
          description: string | null
          id: string
          metadata: Json | null
          organization_id: string | null
          payment_method: string | null
          status: string
          stripe_invoice_id: string | null
          stripe_payment_intent_id: string | null
        }
        Insert: {
          amount: number
          created_at?: string
          currency?: string | null
          description?: string | null
          id?: string
          metadata?: Json | null
          organization_id?: string | null
          payment_method?: string | null
          status: string
          stripe_invoice_id?: string | null
          stripe_payment_intent_id?: string | null
        }
        Update: {
          amount?: number
          created_at?: string
          currency?: string | null
          description?: string | null
          id?: string
          metadata?: Json | null
          organization_id?: string | null
          payment_method?: string | null
          status?: string
          stripe_invoice_id?: string | null
          stripe_payment_intent_id?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "payment_history_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organization_dashboard"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "payment_history_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organizations"
            referencedColumns: ["id"]
          },
        ]
      }
      pipelines: {
        Row: {
          agent_logs: Json | null
          agent_status: Json | null
          agents_completed: Json | null
          article_id: string | null
          cancellation_reason: string | null
          cancelled_by: string | null
          completed_at: string | null
          config: Json | null
          cost_breakdown: Json | null
          created_at: string | null
          current_agent: string | null
          description: string | null
          error_code: string | null
          error_details: Json | null
          error_message: string | null
          estimated_completion: string | null
          estimated_cost: number | null
          execution_time: number | null
          id: string
          max_retries: number | null
          metrics: Json | null
          name: string
          organization_id: string
          priority: number | null
          progress: number | null
          queued_at: string | null
          results: Json | null
          retry_count: number | null
          started_at: string | null
          status: string | null
          template_id: string | null
          total_cost: number | null
          user_id: string
        }
        Insert: {
          agent_logs?: Json | null
          agent_status?: Json | null
          agents_completed?: Json | null
          article_id?: string | null
          cancellation_reason?: string | null
          cancelled_by?: string | null
          completed_at?: string | null
          config?: Json | null
          cost_breakdown?: Json | null
          created_at?: string | null
          current_agent?: string | null
          description?: string | null
          error_code?: string | null
          error_details?: Json | null
          error_message?: string | null
          estimated_completion?: string | null
          estimated_cost?: number | null
          execution_time?: number | null
          id?: string
          max_retries?: number | null
          metrics?: Json | null
          name: string
          organization_id: string
          priority?: number | null
          progress?: number | null
          queued_at?: string | null
          results?: Json | null
          retry_count?: number | null
          started_at?: string | null
          status?: string | null
          template_id?: string | null
          total_cost?: number | null
          user_id: string
        }
        Update: {
          agent_logs?: Json | null
          agent_status?: Json | null
          agents_completed?: Json | null
          article_id?: string | null
          cancellation_reason?: string | null
          cancelled_by?: string | null
          completed_at?: string | null
          config?: Json | null
          cost_breakdown?: Json | null
          created_at?: string | null
          current_agent?: string | null
          description?: string | null
          error_code?: string | null
          error_details?: Json | null
          error_message?: string | null
          estimated_completion?: string | null
          estimated_cost?: number | null
          execution_time?: number | null
          id?: string
          max_retries?: number | null
          metrics?: Json | null
          name?: string
          organization_id?: string
          priority?: number | null
          progress?: number | null
          queued_at?: string | null
          results?: Json | null
          retry_count?: number | null
          started_at?: string | null
          status?: string | null
          template_id?: string | null
          total_cost?: number | null
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "pipelines_article_id_fkey"
            columns: ["article_id"]
            isOneToOne: false
            referencedRelation: "article_performance"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "pipelines_article_id_fkey"
            columns: ["article_id"]
            isOneToOne: false
            referencedRelation: "articles"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "pipelines_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organization_dashboard"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "pipelines_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organizations"
            referencedColumns: ["id"]
          },
        ]
      }
      profiles: {
        Row: {
          account_locked_until: string | null
          avatar_url: string | null
          created_at: string | null
          deleted_at: string | null
          email: string
          failed_login_attempts: number | null
          full_name: string | null
          id: string
          last_activity_at: string | null
          last_login_at: string | null
          last_password_change: string | null
          notification_preferences: Json | null
          onboarding_completed: boolean | null
          onboarding_step: number | null
          organization_id: string | null
          platform_role: string | null
          role: string | null
          timezone: string | null
          two_factor_enabled: boolean | null
          updated_at: string | null
        }
        Insert: {
          account_locked_until?: string | null
          avatar_url?: string | null
          created_at?: string | null
          deleted_at?: string | null
          email: string
          failed_login_attempts?: number | null
          full_name?: string | null
          id: string
          last_activity_at?: string | null
          last_login_at?: string | null
          last_password_change?: string | null
          notification_preferences?: Json | null
          onboarding_completed?: boolean | null
          onboarding_step?: number | null
          organization_id?: string | null
          platform_role?: string | null
          role?: string | null
          timezone?: string | null
          two_factor_enabled?: boolean | null
          updated_at?: string | null
        }
        Update: {
          account_locked_until?: string | null
          avatar_url?: string | null
          created_at?: string | null
          deleted_at?: string | null
          email?: string
          failed_login_attempts?: number | null
          full_name?: string | null
          id?: string
          last_activity_at?: string | null
          last_login_at?: string | null
          last_password_change?: string | null
          notification_preferences?: Json | null
          onboarding_completed?: boolean | null
          onboarding_step?: number | null
          organization_id?: string | null
          platform_role?: string | null
          role?: string | null
          timezone?: string | null
          two_factor_enabled?: boolean | null
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "profiles_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organization_dashboard"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "profiles_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organizations"
            referencedColumns: ["id"]
          },
        ]
      }
      rate_limits: {
        Row: {
          created_at: string | null
          endpoint: string
          id: string
          max_requests: number | null
          method: string
          organization_id: string
          period_end: string | null
          period_start: string | null
          requests_count: number | null
          updated_at: string | null
        }
        Insert: {
          created_at?: string | null
          endpoint: string
          id?: string
          max_requests?: number | null
          method: string
          organization_id: string
          period_end?: string | null
          period_start?: string | null
          requests_count?: number | null
          updated_at?: string | null
        }
        Update: {
          created_at?: string | null
          endpoint?: string
          id?: string
          max_requests?: number | null
          method?: string
          organization_id?: string
          period_end?: string | null
          period_start?: string | null
          requests_count?: number | null
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "rate_limits_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organization_dashboard"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "rate_limits_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organizations"
            referencedColumns: ["id"]
          },
        ]
      }
      schema_migrations: {
        Row: {
          executed_at: string | null
          executed_by: string | null
          version: string
        }
        Insert: {
          executed_at?: string | null
          executed_by?: string | null
          version: string
        }
        Update: {
          executed_at?: string | null
          executed_by?: string | null
          version?: string
        }
        Relationships: []
      }
      subscribers: {
        Row: {
          created_at: string
          email: string
          id: string
          stripe_customer_id: string | null
          stripe_subscription_id: string | null
          subscribed: boolean
          subscription_end: string | null
          subscription_status: string | null
          subscription_tier: string | null
          trial_ends_at: string | null
          updated_at: string
          user_id: string | null
        }
        Insert: {
          created_at?: string
          email: string
          id?: string
          stripe_customer_id?: string | null
          stripe_subscription_id?: string | null
          subscribed?: boolean
          subscription_end?: string | null
          subscription_status?: string | null
          subscription_tier?: string | null
          trial_ends_at?: string | null
          updated_at?: string
          user_id?: string | null
        }
        Update: {
          created_at?: string
          email?: string
          id?: string
          stripe_customer_id?: string | null
          stripe_subscription_id?: string | null
          subscribed?: boolean
          subscription_end?: string | null
          subscription_status?: string | null
          subscription_tier?: string | null
          trial_ends_at?: string | null
          updated_at?: string
          user_id?: string | null
        }
        Relationships: []
      }
      topics: {
        Row: {
          approved_at: string | null
          approved_by: string | null
          assigned_at: string | null
          assigned_to: string | null
          competition_level: string | null
          competitor_coverage: Json | null
          completed_at: string | null
          content_gaps: string[] | null
          cpc: number | null
          difficulty_score: number | null
          id: string
          identified_at: string | null
          keyword: string
          opportunity_score: number | null
          organization_id: string
          questions: string[] | null
          related_keywords: string[] | null
          search_volume: number | null
          status: string | null
          topic_cluster: string | null
          trend: string | null
        }
        Insert: {
          approved_at?: string | null
          approved_by?: string | null
          assigned_at?: string | null
          assigned_to?: string | null
          competition_level?: string | null
          competitor_coverage?: Json | null
          completed_at?: string | null
          content_gaps?: string[] | null
          cpc?: number | null
          difficulty_score?: number | null
          id?: string
          identified_at?: string | null
          keyword: string
          opportunity_score?: number | null
          organization_id: string
          questions?: string[] | null
          related_keywords?: string[] | null
          search_volume?: number | null
          status?: string | null
          topic_cluster?: string | null
          trend?: string | null
        }
        Update: {
          approved_at?: string | null
          approved_by?: string | null
          assigned_at?: string | null
          assigned_to?: string | null
          competition_level?: string | null
          competitor_coverage?: Json | null
          completed_at?: string | null
          content_gaps?: string[] | null
          cpc?: number | null
          difficulty_score?: number | null
          id?: string
          identified_at?: string | null
          keyword?: string
          opportunity_score?: number | null
          organization_id?: string
          questions?: string[] | null
          related_keywords?: string[] | null
          search_volume?: number | null
          status?: string | null
          topic_cluster?: string | null
          trend?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "topics_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organization_dashboard"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "topics_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organizations"
            referencedColumns: ["id"]
          },
        ]
      }
      usage_tracking: {
        Row: {
          amount: number | null
          billing_month: string
          created_at: string
          id: string
          metadata: Json | null
          organization_id: string | null
          resource_id: string | null
          resource_type: string
          usage_count: number | null
          user_id: string | null
        }
        Insert: {
          amount?: number | null
          billing_month?: string
          created_at?: string
          id?: string
          metadata?: Json | null
          organization_id?: string | null
          resource_id?: string | null
          resource_type: string
          usage_count?: number | null
          user_id?: string | null
        }
        Update: {
          amount?: number | null
          billing_month?: string
          created_at?: string
          id?: string
          metadata?: Json | null
          organization_id?: string | null
          resource_id?: string | null
          resource_type?: string
          usage_count?: number | null
          user_id?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "usage_tracking_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organization_dashboard"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "usage_tracking_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organizations"
            referencedColumns: ["id"]
          },
        ]
      }
      webhook_logs: {
        Row: {
          created_at: string | null
          delivered: boolean | null
          delivered_at: string | null
          error_message: string | null
          event_type: string
          headers: Json | null
          id: string
          max_retries: number | null
          next_retry_at: string | null
          organization_id: string
          payload: Json
          response_body: string | null
          response_headers: Json | null
          retry_count: number | null
          status: string | null
          status_code: number | null
          webhook_url: string
        }
        Insert: {
          created_at?: string | null
          delivered?: boolean | null
          delivered_at?: string | null
          error_message?: string | null
          event_type: string
          headers?: Json | null
          id?: string
          max_retries?: number | null
          next_retry_at?: string | null
          organization_id: string
          payload: Json
          response_body?: string | null
          response_headers?: Json | null
          retry_count?: number | null
          status?: string | null
          status_code?: number | null
          webhook_url: string
        }
        Update: {
          created_at?: string | null
          delivered?: boolean | null
          delivered_at?: string | null
          error_message?: string | null
          event_type?: string
          headers?: Json | null
          id?: string
          max_retries?: number | null
          next_retry_at?: string | null
          organization_id?: string
          payload?: Json
          response_body?: string | null
          response_headers?: Json | null
          retry_count?: number | null
          status?: string | null
          status_code?: number | null
          webhook_url?: string
        }
        Relationships: [
          {
            foreignKeyName: "webhook_logs_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organization_dashboard"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "webhook_logs_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organizations"
            referencedColumns: ["id"]
          },
        ]
      }
    }
    Views: {
      article_performance: {
        Row: {
          author_email: string | null
          author_name: string | null
          engagement_rate: number | null
          generation_cost: number | null
          id: string | null
          organization_id: string | null
          published_at: string | null
          readability_score: number | null
          seo_score: number | null
          shares_count: number | null
          status: string | null
          title: string | null
          views_count: number | null
          word_count: number | null
        }
        Relationships: [
          {
            foreignKeyName: "articles_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organization_dashboard"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "articles_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organizations"
            referencedColumns: ["id"]
          },
        ]
      }
      article_stats: {
        Row: {
          avg_seo_score: number | null
          avg_word_count: number | null
          draft_articles: number | null
          organization_id: string | null
          published_articles: number | null
          total_articles: number | null
          total_cost: number | null
        }
        Relationships: [
          {
            foreignKeyName: "articles_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organization_dashboard"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "articles_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organizations"
            referencedColumns: ["id"]
          },
        ]
      }
      cost_analysis: {
        Row: {
          api_calls: number | null
          avg_cost_per_call: number | null
          billing_month: string | null
          max_cost: number | null
          min_cost: number | null
          organization_id: string | null
          service: string | null
          total_cost: number | null
          total_tokens: number | null
        }
        Relationships: [
          {
            foreignKeyName: "cost_tracking_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organization_dashboard"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "cost_tracking_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organizations"
            referencedColumns: ["id"]
          },
        ]
      }
      organization_dashboard: {
        Row: {
          active_pipelines: number | null
          articles_limit: number | null
          articles_used: number | null
          budget_percentage: number | null
          completed_pipelines: number | null
          current_month_cost: number | null
          draft_articles: number | null
          id: string | null
          monthly_budget: number | null
          name: string | null
          plan: string | null
          published_articles: number | null
          slug: string | null
          subscription_status: string | null
          team_members: number | null
          trial_ends_at: string | null
        }
        Relationships: []
      }
      pipeline_stats: {
        Row: {
          avg_execution_time: number | null
          failed_runs: number | null
          organization_id: string | null
          successful_runs: number | null
          total_cost: number | null
          total_runs: number | null
        }
        Relationships: [
          {
            foreignKeyName: "pipelines_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organization_dashboard"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "pipelines_organization_id_fkey"
            columns: ["organization_id"]
            isOneToOne: false
            referencedRelation: "organizations"
            referencedColumns: ["id"]
          },
        ]
      }
      recent_activity: {
        Row: {
          activity_id: string | null
          activity_type: string | null
          description: string | null
          details: Json | null
          occurred_at: string | null
          organization_id: string | null
          user_id: string | null
        }
        Relationships: []
      }
    }
    Functions: {
      binary_quantize: {
        Args: { "": string } | { "": unknown }
        Returns: unknown
      }
      check_budget_limit: {
        Args: { p_organization_id: string }
        Returns: boolean
      }
      check_rate_limit: {
        Args: {
          p_endpoint: string
          p_method?: string
          p_organization_id: string
        }
        Returns: boolean
      }
      get_system_health: {
        Args: Record<PropertyKey, never>
        Returns: {
          details: Json
          metric: string
          status: string
          value: number
        }[]
      }
      halfvec_avg: {
        Args: { "": number[] }
        Returns: unknown
      }
      halfvec_out: {
        Args: { "": unknown }
        Returns: unknown
      }
      halfvec_send: {
        Args: { "": unknown }
        Returns: string
      }
      halfvec_typmod_in: {
        Args: { "": unknown[] }
        Returns: number
      }
      hnsw_bit_support: {
        Args: { "": unknown }
        Returns: unknown
      }
      hnsw_halfvec_support: {
        Args: { "": unknown }
        Returns: unknown
      }
      hnsw_sparsevec_support: {
        Args: { "": unknown }
        Returns: unknown
      }
      hnswhandler: {
        Args: { "": unknown }
        Returns: unknown
      }
      ivfflat_bit_support: {
        Args: { "": unknown }
        Returns: unknown
      }
      ivfflat_halfvec_support: {
        Args: { "": unknown }
        Returns: unknown
      }
      ivfflathandler: {
        Args: { "": unknown }
        Returns: unknown
      }
      l2_norm: {
        Args: { "": unknown } | { "": unknown }
        Returns: number
      }
      l2_normalize: {
        Args: { "": string } | { "": unknown } | { "": unknown }
        Returns: unknown
      }
      sparsevec_out: {
        Args: { "": unknown }
        Returns: unknown
      }
      sparsevec_send: {
        Args: { "": unknown }
        Returns: string
      }
      sparsevec_typmod_in: {
        Args: { "": unknown[] }
        Returns: number
      }
      vector_avg: {
        Args: { "": number[] }
        Returns: string
      }
      vector_dims: {
        Args: { "": string } | { "": unknown }
        Returns: number
      }
      vector_norm: {
        Args: { "": string }
        Returns: number
      }
      vector_out: {
        Args: { "": string }
        Returns: unknown
      }
      vector_send: {
        Args: { "": string }
        Returns: string
      }
      vector_typmod_in: {
        Args: { "": unknown[] }
        Returns: number
      }
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  public: {
    Enums: {},
  },
} as const
