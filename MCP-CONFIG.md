# Supabase MCP Configuration for Antigravity

## Your Custom MCP Configuration

Add this to your Antigravity MCP settings:

### Option 1: Read-Only Mode (Recommended for Safety)
```json
{
  "mcpServers": {
    "supabase-himap": {
      "type": "http",
      "url": "https://mcp.supabase.com/mcp?read_only=true&project_ref=llvsayyfvwkqbmhnmumh&features=database,docs"
    }
  }
}
```

**What this enables:**
- ✅ Read-only database access (no accidental modifications)
- ✅ View tables, schemas, and data
- ✅ Execute SELECT queries
- ✅ Search Supabase documentation
- ❌ No write operations (INSERT, UPDATE, DELETE)

### Option 2: Full Access Mode (Use with Caution)
```json
{
  "mcpServers": {
    "supabase-himap": {
      "type": "http",
      "url": "https://mcp.supabase.com/mcp?project_ref=llvsayyfvwkqbmhnmumh&features=database,docs,development"
    }
  }
}
```

**What this enables:**
- ✅ Full database access (read and write)
- ✅ Apply migrations
- ✅ Execute any SQL
- ✅ Generate TypeScript types
- ⚠️ Can modify your database

## Next Steps

1. **Add MCP Configuration to Antigravity**
   - Check Antigravity documentation for MCP configuration location
   - Add the JSON above to your MCP settings
   - Restart Antigravity if needed

2. **Authenticate with Supabase**
   - Antigravity will prompt you to log in to Supabase
   - Choose the organization that contains project `llvsayyfvwkqbmhnmumh`
   - Grant access permissions

3. **Test the Connection**
   - Once configured, I'll be able to:
     - List your database tables
     - View the HIMAP member data
     - Execute queries directly
     - Help with schema migrations

4. **Update Frontend Configuration**
   - Get your **Anon Key** from Supabase Dashboard > Project Settings > API
   - Update `supabase-config.js` with the anon key (URL is already set)

## Project Details

- **Project ID**: `llvsayyfvwkqbmhnmumh`
- **Project URL**: `https://llvsayyfvwkqbmhnmumh.supabase.co`
- **Database**: Ready for HIMAP member directory (10 tables)

## What I Can Do Once Connected

✅ **Database Management**
- List all tables in your HIMAP database
- View table schemas and relationships
- Execute SQL queries to fetch member data
- Help debug database issues

✅ **Development Support**
- Generate TypeScript types from your schema
- Create and test SQL migrations
- Query logs for debugging
- Search Supabase documentation

✅ **Data Operations** (if using full access mode)
- Insert HIMAP member data
- Update company information
- Manage certifications and personnel records
- Bulk import operations
