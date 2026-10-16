# Custom domain on GitHub Pages

Goal: `yourdomain.com` and `www.yourdomain.com` both show your site over HTTPS.

You need: a published site at `yourname.github.io` and a domain bought from any registrar.
Menu names below vary by registrar. Look for "DNS", "DNS zone" or "DNS records".

Replace `yourname` with your GitHub user name and `yourdomain.com` with your domain.

## Order matters

1. Verify the domain for your GitHub account (step 1).
2. Point DNS at GitHub (step 2).
3. Only then add the domain to the repository (step 4).

Verifying first stops anyone else from claiming your domain for their Pages site if your repository is ever deleted.

DNS changes can take from minutes up to 24 hours to spread. Do not start this the night before you need it.

## Step 1. Verify the domain for your account

This is in your **account** settings, not the repository's.

1. github.com, your picture top right, **Settings**, left menu **Pages**.
2. **Add a domain**, type `yourdomain.com`, **Add domain**.
3. GitHub shows a TXT record: a name like `_github-pages-challenge-yourname` and a random value. Copy both.
4. In your registrar's DNS editor, add a record:
   - Type: `TXT`
   - Name: `_github-pages-challenge-yourname`. Most editors add the domain themselves, so do not type it.
   - Value: the random string from GitHub
5. Wait at least 15 minutes. Check in PowerShell:

```powershell
Resolve-DnsName -Name _github-pages-challenge-yourname.yourdomain.com -Type TXT
```

**Mac/Linux:** `dig TXT _github-pages-challenge-yourname.yourdomain.com +short`

6. When the value shows, go back to GitHub and click **Verify**.
7. Leave the TXT record in place permanently.

## Step 2. Point DNS at GitHub

1. Delete any existing A record for `@` (the bare domain). Registrars often add one for a parking page.
2. Add four **A** records. Name `@`, one value each:

| Value           |
| --------------- |
| 185.199.108.153 |
| 185.199.109.153 |
| 185.199.110.153 |
| 185.199.111.153 |

3. Add four **AAAA** records (IPv6). Optional, but without them IPv6-only visitors cannot reach the site. Name `@`:

| Value               |
| ------------------- |
| 2606:50c0:8000::153 |
| 2606:50c0:8001::153 |
| 2606:50c0:8002::153 |
| 2606:50c0:8003::153 |

4. Set **www**: type `CNAME`, name `www`, target `yourname.github.io`. No repository name in the target.
5. If your registrar has a CDN or proxy switched on for the domain, switch it off.

Check these addresses against GitHub's current documentation before you start (link below). They have been stable for years, but GitHub owns them.

## Step 3. Wait and check

```powershell
Resolve-DnsName -Name yourdomain.com -Type A
Resolve-DnsName -Name yourdomain.com -Type AAAA
Resolve-DnsName -Name www.yourdomain.com -Type CNAME
```

Expected: the four IPv4 addresses, the four IPv6 addresses, and `www` pointing to `yourname.github.io`.
If your computer still shows old values: `ipconfig /flushdns`.

## Step 4. Add the domain to the repository

1. Your repository, **Settings** tab, left menu **Pages**.
2. **Custom domain:** `yourdomain.com`, **Save**.
3. Wait for the DNS check to turn green.

Also put the domain in `settings.json`, `"domain": "yourdomain.com"`. Then `build.py` writes `sitemap.txt` with full addresses, and a `CNAME` file.

| Publishing option | Is the `CNAME` file needed? |
| ----------------- | --------------------------- |
| A, GitHub Actions in one repo | No. The Settings field is what counts |
| B, two repos, push to a branch | Yes. Without it the domain is dropped on every deploy |

## Step 5. HTTPS

1. Same page. Wait until **Enforce HTTPS** can be ticked. GitHub fetches a free certificate. Minutes to an hour.
2. Tick **Enforce HTTPS**.
3. If it stays grey, wait. Do not remove and re-add the domain: it starts over.

## Step 6. Final check

All four should end on the same page, with a lock icon:

1. `http://yourdomain.com`
2. `https://yourdomain.com`
3. `http://www.yourdomain.com`
4. `https://www.yourdomain.com`

## Undo

Delete the four A and four AAAA records and put back your registrar's original A record. Keep the TXT record.

Problems: [TROUBLESHOOTING.md](TROUBLESHOOTING.md), section 7.

## Sources

- GitHub Docs, Managing a custom domain for your GitHub Pages site: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- GitHub Docs, Verifying your custom domain for GitHub Pages: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages
- GitHub Docs, Troubleshooting custom domains and GitHub Pages: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/troubleshooting-custom-domains-and-github-pages
