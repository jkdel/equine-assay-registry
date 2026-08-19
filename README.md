# Equine Assay Registry

Read more about [the equine assay registry here](https://www.equine-assay-registry.org).
Below we explain the technical aspects of the project and how to make it your
own. This code can be adapted to build collaborative registries for any
structured text-based dataset requiring community submissions, transparent
review workflows, DOI assignment, and static website publication.

## What it does

- Browse JSON records through a static Jekyll website hosted on GitHub/Vercel
- Submit new records through a web form that automatically generates GitHub pull
  requests via a Vercel serverless function
- Review submissions using GitHub's pull request workflow
- Mint DOIs for accepted original submissions through Figshare
- Client-side RSA-OAEP encryption of sensitive contributor information
- Fully serverless architecture (GitHub, Vercel, and Figshare)
- Transparent version control and review process
- Extensible to any text-based research registry or structured dataset

## FAIR Principles

The registry architecture supports FAIR data practices through:

- Persistent identifiers (DOIs) for accepted original submissions
- Open, machine- and human-readable metadata stored as JSON
- Version-controlled data through git
- Long-term archival through Figshare

## Architecture

```text
 ┌────────────────────────────────┐ 
 │ Submission form                │ 
 └────────────────┬───────────────┘ 
 ┌────────────────▼───────────────┐ 
 │ Vercel serverless function     │ 
 └────────────────┬───────────────┘ 
 ┌────────────────▼───────────────┐ 
 │ GitHub pull request            │ 
 └────────────────┬───────────────┘ 
 ┌────────────────▼───────────────┐ 
 │ Review and merge               │ 
 └────────────────┬───────────────┘ 
 ┌────────────────▼───────────────┐ 
 │ GitHub action                  │ 
 │   - Upload files to Figshare   │ 
 │   - Mint DOI                   │ 
 │   - Update submission metadata │ 
 └────────────────┬───────────────┘ 
 ┌────────────────▼───────────────┐ 
 │ Jekyll static website          │ 
 └────────────────────────────────┘ 
```

## Deployment

1. Fork this repository
2. Create a Figshare token and add as github secret (FIGSHARE_TOKEN)
3. Add repository to vercel with Jekkyl framework
4. Create a Github PAT token (Read and Write access to code and pull requests)
   and add it to Vercel environment secrets as GITHUB_TOKEN alongside
   GITHUB_REPO_OWNER and GITHUB_REPO_NAME
5. Modify and test locally
    1. `git clone FORK_URL`
    2. `npm install`
    3. `npx vercel dev`
6. Replace the encryption key with your own ([see encryption.md](./encryption.md))
7. Adapt the submission schema, Jekyll templates, and review workflow to your
   use case
8. Optional: add your domain name

## Use of artificial intelligence (AI)

Different large language models were used to draft parts of the code. The AI
generated code snippets were tested and implemented manually by the author of
the repository.
