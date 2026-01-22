# Deploy Project

Deploy the project to a target environment.

## Usage
```
/project-deploy [environment]
```

## Arguments

- `$ARGUMENTS` - Target environment: `development`, `staging`, `production`, or server details

## Workflow

1. **Determine Deployment Target**
   - Ask: "Where are you deploying to?"
   - Options: Linux server, Docker, Android, iOS, Web hosting

2. **Check Prerequisites**
   - Verify build passes
   - Run tests
   - Check for security issues

3. **Execute Deployment**
   - Invoke Platform Installer Agent
   - Configure services (Nginx, SSL, etc.)
   - Set up Cloudflare if needed

4. **Verify Deployment**
   - Run health checks
   - Verify endpoints respond
   - Check logs for errors

5. **Document**
   - Update deployment notes
   - Record in Learning System

## Examples

```
# Deploy to staging
/project-deploy staging

# Deploy to production server
/project-deploy production 192.168.1.100

# Deploy to Docker
/project-deploy docker
```

## Related Agents

- Platform Installer Agent
- Cloudflare Agent
- Security Audit Agent
- Monitoring Agent
