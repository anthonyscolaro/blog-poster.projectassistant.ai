#!/bin/bash

# Supabase Sync Script
# Syncs data from Lovable's Supabase cloud to local Docker Supabase

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Configuration
CLOUD_SUPABASE_URL="${CLOUD_SUPABASE_URL:-https://epftkydwdqerdlhvqili.supabase.co}"
CLOUD_SUPABASE_ANON_KEY="${CLOUD_SUPABASE_ANON_KEY:-eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0}"

LOCAL_SUPABASE_URL="http://localhost:8000"
LOCAL_DB_HOST="localhost"
LOCAL_DB_PORT="5434"
LOCAL_DB_NAME="postgres"
LOCAL_DB_USER="postgres"
LOCAL_DB_PASSWORD="your-super-secret-password"

# Export schema from cloud
export_cloud_schema() {
    print_status "Exporting schema from cloud Supabase..."
    
    # Use supabase CLI to export schema
    npx supabase db dump \
        --db-url "postgresql://postgres.epftkydwdqerdlhvqili:${CLOUD_SUPABASE_PASSWORD}@aws-0-us-west-1.pooler.supabase.com:5432/postgres" \
        --schema public \
        --schema auth \
        --schema storage \
        > cloud_schema.sql
    
    print_status "Schema exported to cloud_schema.sql"
}

# Export data from cloud
export_cloud_data() {
    print_status "Exporting data from cloud Supabase..."
    
    # Export specific tables
    tables=(
        "organizations"
        "profiles"
        "articles"
        "pipelines"
        "api_keys"
        "team_members"
        "team_invitations"
        "billing_plans"
        "subscriptions"
        "activity_logs"
    )
    
    for table in "${tables[@]}"; do
        print_status "Exporting table: $table"
        
        # Use pg_dump to export data
        PGPASSWORD="${CLOUD_SUPABASE_PASSWORD}" pg_dump \
            -h aws-0-us-west-1.pooler.supabase.com \
            -p 5432 \
            -U postgres.epftkydwdqerdlhvqili \
            -d postgres \
            --table=public.$table \
            --data-only \
            --column-inserts \
            > "data_${table}.sql"
    done
    
    print_status "Data export complete"
}

# Import to local Supabase
import_to_local() {
    print_status "Importing to local Supabase..."
    
    # Wait for local database to be ready
    print_status "Waiting for local database..."
    for i in {1..30}; do
        if PGPASSWORD=$LOCAL_DB_PASSWORD psql -h $LOCAL_DB_HOST -p $LOCAL_DB_PORT -U $LOCAL_DB_USER -d $LOCAL_DB_NAME -c "SELECT 1" >/dev/null 2>&1; then
            break
        fi
        echo -n "."
        sleep 2
    done
    echo ""
    
    # Import schema
    print_status "Importing schema..."
    PGPASSWORD=$LOCAL_DB_PASSWORD psql \
        -h $LOCAL_DB_HOST \
        -p $LOCAL_DB_PORT \
        -U $LOCAL_DB_USER \
        -d $LOCAL_DB_NAME \
        < cloud_schema.sql
    
    # Import data
    for table in "${tables[@]}"; do
        if [ -f "data_${table}.sql" ]; then
            print_status "Importing data for table: $table"
            PGPASSWORD=$LOCAL_DB_PASSWORD psql \
                -h $LOCAL_DB_HOST \
                -p $LOCAL_DB_PORT \
                -U $LOCAL_DB_USER \
                -d $LOCAL_DB_NAME \
                < "data_${table}.sql"
        fi
    done
    
    print_status "Import complete"
}

# Main sync process
main() {
    print_status "Starting Supabase sync from cloud to local..."
    
    # Check if cloud password is provided
    if [ -z "$CLOUD_SUPABASE_PASSWORD" ]; then
        print_error "CLOUD_SUPABASE_PASSWORD environment variable is required"
        print_warning "Get this from your Supabase dashboard > Settings > Database"
        exit 1
    fi
    
    # Check if local Supabase is running
    if ! docker ps | grep -q "supabase-db"; then
        print_warning "Local Supabase is not running. Starting it now..."
        docker compose up -d supabase-db
        sleep 10
    fi
    
    # Create backup directory
    backup_dir="supabase_backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    cd "$backup_dir"
    
    # Run sync steps
    export_cloud_schema
    export_cloud_data
    import_to_local
    
    print_status "Sync complete! Backup saved in $backup_dir"
    
    # Test connection
    print_status "Testing local Supabase connection..."
    if curl -s "$LOCAL_SUPABASE_URL/rest/v1/" > /dev/null; then
        print_status "Local Supabase is accessible at $LOCAL_SUPABASE_URL"
    else
        print_warning "Could not reach local Supabase API"
    fi
}

# Handle command line arguments
case "$1" in
    export)
        export_cloud_schema
        export_cloud_data
        ;;
    import)
        import_to_local
        ;;
    test)
        print_status "Testing connections..."
        # Test cloud
        if curl -s "$CLOUD_SUPABASE_URL/rest/v1/" > /dev/null; then
            print_status "Cloud Supabase is accessible"
        else
            print_error "Cannot reach cloud Supabase"
        fi
        # Test local
        if curl -s "$LOCAL_SUPABASE_URL/rest/v1/" > /dev/null; then
            print_status "Local Supabase is accessible"
        else
            print_error "Cannot reach local Supabase"
        fi
        ;;
    *)
        main
        ;;
esac