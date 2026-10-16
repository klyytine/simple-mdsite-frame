# Option B: private source, public site

Use this when you want your Markdown, drafts and history private, and only the finished HTML public.

On the free GitHub plan, Pages publishes only from public repositories.
So you keep two:

| Repository | Visibility | Holds |
| ---------- | ---------- | ----- |
| `my-site-source` | Private | Everything in this frame |
| `yourname.github.io` | Public | Only the built `dist/` files, one commit, replaced on each deploy |

```mermaid
flowchart LR
  A["You: git push"] --> B["Private repo<br/>my-site-source"]
  B --> C["Actions: build.py"]
  C -->|"deploy key, force push"| D["Public repo<br/>yourname.github.io"]
  D --> E["GitHub Pages"]
```

You need the GitHub CLI for the commands below: https://cli.github.com. Sign in once with `gh auth login`.

## What a deploy key is

An SSH key that opens **one** repository only. It has two halves:

| Half | Where it goes | Role |
| ---- | ------------- | ---- |
| Public (`.pub`) | Public repo, Settings, Deploy keys, with **Allow write access** | The lock |
| Private | Private repo, as the Actions secret `PAGES_DEPLOY_KEY` | The key |

If the private half leaks, someone can overwrite your public site, nothing more. Your source stays private.
Deploy keys do not expire. Replace the key if you suspect a leak.

## Setup

Run in PowerShell from your site folder. Replace `yourname`.

**1. Create the public repo**, with Pages from a branch:

```powershell
gh repo create yourname/yourname.github.io --public --add-readme
```

Then on github.com: that repo, Settings, Pages, Source **Deploy from a branch**, branch `main`, folder `/ (root)`.

**2. Move the workflow.** Replace option A with option B:

```powershell
Copy-Item docs\optional\deploy-two-repo.yml .github\workflows\deploy.yml -Force
```

Open `.github\workflows\deploy.yml` and fill the three `CHANGE_ME` values:

- `PUBLIC_REPO`: `yourname/yourname.github.io`
- `BOT_EMAIL`: your noreply address from GitHub, Settings, Emails

**3. Create the private source repo** from this folder:

```powershell
git add -A
git commit -m "Switch to two-repo deploy"
gh repo create yourname/my-site-source --private --source . --push
```

If this folder is already a clone of another repo, first point it elsewhere: `git remote remove origin`.

**4. Make the key pair.** No passphrase, because a robot uses it:

```powershell
ssh-keygen -t ed25519 -C "site-deploy" -f "$HOME\.ssh\site_deploy" -N '""'
```

**5. Public half to the public repo, with write access:**

```powershell
gh repo deploy-key add "$HOME\.ssh\site_deploy.pub" --repo yourname/yourname.github.io --allow-write --title "site-deploy"
```

**6. Private half to the private repo as a secret:**

```powershell
Get-Content "$HOME\.ssh\site_deploy" -Raw | gh secret set PAGES_DEPLOY_KEY --repo yourname/my-site-source
```

**7. Delete both key files from your computer.** GitHub keeps the secret encrypted.

```powershell
Remove-Item "$HOME\.ssh\site_deploy", "$HOME\.ssh\site_deploy.pub"
```

**8. Test:** push any change to the private repo. Its Actions tab should show a green tick, and the public repo a new commit.

## Custom domain with option B

Set `"domain"` in `settings.json`. `build.py` then writes `CNAME` into every build.
Without it, GitHub Pages drops the custom domain on each deploy, because the push replaces all files.

## Replacing the key

Public repo, Settings, Deploy keys: delete the old key. Then repeat steps 4 to 7.

Problems: [TROUBLESHOOTING.md](TROUBLESHOOTING.md), section 6, "Option B only".

## Sources

- GitHub Docs, Managing deploy keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managing-deploy-keys
- GitHub Docs, Configuring a publishing source for your GitHub Pages site: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- GitHub Docs, Using secrets in GitHub Actions: https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions
