# Troubleshooting

Find your symptom, read the cause, apply the fix.
Most of these were met while building and publishing a real site with this frame.

Sections:

1. Tools not found
2. Python and the virtual environment
3. Building
4. Pages, menu and links
5. git and pushing
6. GitHub Actions and Pages
7. Custom domain, DNS and HTTPS
8. After moving the site folder

---

## 1. Tools not found

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| `python : The term 'python' is not recognized` | Python is not installed, or "Add python.exe to PATH" was not ticked | Re-run the Python installer, choose **Modify**, tick **Add Python to environment variables**. Close and reopen the terminal |
| Typing `python` opens the Microsoft Store | Windows has a placeholder `python` command | Install Python from python.org. Then Windows Settings, **Apps**, **Advanced app settings**, **App execution aliases**: turn off both `python.exe` and `python3.exe` |
| `git : The term 'git' is not recognized` | Git is not installed, or the terminal was opened before installing | Install Git. Close every terminal and open a new one |
| A command worked yesterday, not today | The terminal was opened in a different folder | `cd` into the site folder first. `pwd` shows where you are |

## 2. Python and the virtual environment

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| `ModuleNotFoundError: No module named 'markdown'` (or `yaml`) | You ran the system Python, not the project's `.venv` | Activate first: `.\.venv\Scripts\Activate.ps1`. Or run it directly: `.\.venv\Scripts\python.exe build.py` |
| Same error, and `.venv` is active | Packages were never installed in this `.venv` | `pip install -r requirements.txt` |
| `Activate.ps1 cannot be loaded because running scripts is disabled on this system` | PowerShell blocks scripts by default | Run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, answer `Y`. Or use the direct path `.\.venv\Scripts\python.exe` and skip activation |
| `.venv` worked, then stopped after the folder was moved or renamed | A venv stores its own folder path inside it. It cannot be moved | Delete `.venv` and create it again (ABC guide, Part 3) |
| `python` points to a different version than expected | Several Pythons installed | Use the `.venv` path, it always uses the version it was made with. Windows: `py -0` lists installed versions |

## 3. Building

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| `build.py: error: settings.json line N column M` | A JSON mistake, usually a missing or extra comma, or a missing quote | Go to line N. Every list item ends with `,` except the last. Every text value is in `"double quotes"` |
| `front matter in x.md is not valid YAML` | A mistake between the `---` lines | Every line is `key: value` with a space after the colon. A value containing `:` needs quotes: `title: "Part 1: start"` |
| `note: no translation file about.fi.md` | One language file is missing | Create the file, or ignore it: the page is skipped for that language only |
| `language "sv" has no UI block` | You added a language to `settings.json` but not to `build.py` | Copy the `"en"` block in `UI` at the top of `build.py`, rename it `"sv"`, translate the words |
| `Address already in use` with `--serve` | An earlier preview is still running, or another program uses port 8000 | Close the other terminal, or use another port: `python build.py --serve --port 8001` |
| Strange characters (`Ã¤` instead of `ä`) | The file was saved in a non-UTF-8 encoding | In VS Code: bottom bar, encoding, **Save with Encoding**, **UTF-8** |

## 4. Pages, menu and links

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| New page not in the menu | No entry in `settings.json`, or `"visible": false` | Add the entry (ABC guide, 5.3). Check `visible` |
| Page in the menu but shows 404 | `slug` and file name differ, for example `Blog` vs `blog.en.md` | Make them identical, lowercase |
| Page only in the footer | `"footer_only": true` | Remove that line to show it in the menu |
| Links work on the live site but not when opening `dist\index.html` from disk | Links written without the leading `/`, or to `.md` files | Write `/about.html`, not `about.md` or `about`. `build.py` makes `/...` links relative |
| Picture not shown | Wrong path or wrong letter case. GitHub Pages is case-sensitive, Windows is not | Use `/assets/img/name.png` and match the file name exactly, `Photo.PNG` is not `photo.png` |
| Old version still shows after editing | Browser cache | **Ctrl+F5** |
| Mobile menu is open when the page loads | By design: the same element is always open on desktop. No JavaScript is used to close it | Leave it, or style it differently in `site.css` |

## 5. git and pushing

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| `fatal: not a git repository` | You are not inside the cloned folder | `cd` into the folder that contains `.git` |
| `Please tell me who you are` | Name and e-mail not set | ABC guide, 1.5 |
| `git push` asks for a password, and your GitHub password is refused | GitHub does not accept passwords for git. A browser sign-in or token is needed | Git for Windows normally opens a browser sign-in. If you use the GitHub CLI `gh`, run once: `gh auth setup-git` |
| `! [rejected] main -> main (fetch first)` or `non-fast-forward` | GitHub has commits you do not have, for example an edit made on github.com or from another computer | `git pull`, then `git push`. **Do not** jump to `--force`: it replaces everything on GitHub with your copy |
| `git pull` says `CONFLICT` | The same lines were changed in two places | Open the file, keep the right text, delete the `<<<<<<<`, `=======`, `>>>>>>>` lines, then `git add -A`, `git commit`, `git push` |
| An old guide tells you to use `git push --force` | Only needed for a publish repo that is rebuilt from scratch each time (option B does this for you) | For normal updates use plain `git push` |
| You committed a secret (password, token, key) | It is now in the history, even if you delete the file | Revoke or change the secret **first**, on the service it belongs to. Deleting the file does not remove it from history |
| `git push` is slow or fails on a large file | Big videos or images | Keep files small. Put videos on YouTube and embed them. GitHub blocks files over 100 MB |

## 6. GitHub Actions and Pages

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| Red cross on the first run, step **Configure Pages**, "Get Pages site failed" | Pages was not turned on yet | Settings, Pages, Source: **GitHub Actions**. Then Actions tab, the failed run, **Re-run all jobs** |
| Red cross in **Install dependencies** | `requirements.txt` changed or has a typo | Compare with the original file in this frame |
| Red cross in **Build site** | The same error you would get locally | Run `python build.py` on your computer, fix the error it prints, push again |
| Green tick but the site shows 404 | Pages source is "Deploy from a branch" pointing at a branch with no `index.html` | Settings, Pages, Source: **GitHub Actions** |
| Site lives at `yourname.github.io/repo-name/` instead of `yourname.github.io` | The repository is not named `yourname.github.io` | Rename it in Settings, General. Or accept the longer address: links still work because they are relative |
| Pages settings say Pages is unavailable | The repository is private on the free plan | Make it public, or use option B ([TWO_REPO_DEPLOY.md](TWO_REPO_DEPLOY.md)) |
| Nothing happens after push | Pushed to a branch other than `main`, or Actions disabled | `git branch` shows your branch. Settings, Actions, General: allow actions |
| You never notice failures | Actions fail quietly | GitHub e-mails you on failure by default. Check the Actions tab after each push |

Option B only:

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| `Secret PAGES_DEPLOY_KEY is missing` | The secret was not added, or added to the wrong repo | It belongs in the **private source** repo, Settings, Secrets and variables, Actions |
| `Permission denied (publickey)` or `ERROR: The key you are authenticating with has been marked as read only` | Deploy key missing on the public repo, or **Allow write access** not ticked | Public repo, Settings, Deploy keys: add the `.pub` half with **Allow write access** |
| Custom domain disappears after each deploy | `CNAME` was not in the pushed files | Set `"domain"` in `settings.json`. `build.py` then writes `CNAME` on every build |

## 7. Custom domain, DNS and HTTPS

Full setup: [CUSTOM_DOMAIN.md](CUSTOM_DOMAIN.md).

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| Browser still shows the registrar's parking page | The old A record is still there, or still cached | Delete the old A record in your DNS editor. Windows: `ipconfig /flushdns`. Wait |
| GitHub: "Domain does not resolve to the GitHub Pages server" | A records missing or not spread yet | Check with `Resolve-DnsName yourdomain.com -Type A`. Wait, then **Check again** |
| **Verify** refuses the domain | The TXT record name includes the domain twice | Most DNS editors add the domain themselves. Type only `_github-pages-challenge-yourname` |
| Verification lapses later | The TXT record was deleted | Keep the TXT record permanently |
| `www` works, the bare domain does not (or the reverse) | A/AAAA records wrong, or `www` CNAME wrong | Bare domain: four A records (and four AAAA). `www`: CNAME to `yourname.github.io` |
| `www` ignores your CNAME | The registrar's CDN or proxy is on | Turn the CDN off for this domain |
| **Enforce HTTPS** box missing | Pages not active, or no custom domain saved yet | Check in order: repo has content, Pages source set, custom domain saved and DNS check green |
| **Enforce HTTPS** greyed out for hours | GitHub is still getting the certificate. Can take up to an hour or more | Wait. Do not remove and re-add the domain, that restarts the process |
| Still greyed out after a day | A CAA record blocks Let's Encrypt | Check CAA records at your registrar. Remove the domain from Pages and add it again, once |

## 8. After moving the site folder

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| Python errors right after moving | `.venv` cannot be moved | Delete `.venv`, redo ABC guide Part 3 |
| VS Code terminal says the path does not exist | The window still points at the old folder | **File**, **Open Folder**, pick the new location |
| git history gone | `.git` was not moved with the folder (it is hidden) | Move the whole folder, including hidden items. In Explorer: **View**, **Show**, **Hidden items** |
| Notes or guides point to old paths | Paths were written into documents | Search your notes for the old folder name and update them |

---

Still stuck? Copy the **full** error message, not only the last line, and search for it, or open an issue in this repository.
