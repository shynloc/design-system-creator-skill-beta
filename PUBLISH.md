# Publish this Skill to GitHub

Recommended repository slug:

```text
design-system-creator-skill-beta
```

Recommended visibility: **Public**

Recommended description:

```text
A multimodal, evidence-bound Agent Skill that turns personal taste into a reusable Design Kernel and creates consistent Web, DOCX, PPTX, XLSX, PDF and chart experiences.
```

## With GitHub CLI

From this repository root:

```bash
gh auth status
gh repo create design-system-creator-skill-beta \
  --public \
  --description "A multimodal, evidence-bound Agent Skill that turns personal taste into a reusable Design Kernel and creates consistent Web, DOCX, PPTX, XLSX, PDF and chart experiences." \
  --source . \
  --remote origin \
  --push
```

If the repository already exists:

```bash
git init
git add .
git commit -m "Release Design System Creator 1.0.0-beta.1"
git branch -M main
git remote add origin https://github.com/<owner>/design-system-creator-skill-beta.git
git push -u origin main
```

Do not publish secrets, private reference images, local project workspaces, or generated user Design Kernels unless the owner explicitly intends to make them public.
