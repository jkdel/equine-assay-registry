import formidable from 'formidable';
import fs from 'fs';
import { Octokit } from "@octokit/rest";
import { createPullRequest } from "octokit-plugin-create-pull-request";

const MyOctokit = Octokit.plugin(createPullRequest);
// Vercel parses the body by default
export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  const form = formidable({
    multiples: true, 
    keepExtensions: true,
    maxFileSize: 4.5 * 1024 * 1024
  });

  try {
    const [fields, files] = await form.parse(req);
    const sub = JSON.parse(fields.data);
    const filesToUpdate = [];
    filesToUpdate[`_data/submissions/${sub.id}.json`] = JSON.stringify(sub, null, 2);

    if (files.length > 0 && files.files.length>0) {
      for (const file of files.files) {
        filesToUpdate[`_data/supplementary/${sub.id}/${file.originalFilename.replace(/[^a-z0-9.\-_]/gi, '_')}`] = {
          content: fs.readFileSync(file.filepath, 'base64'),
          encoding: "base64" 
        };
      }
    };
    
    const octokit = new MyOctokit({ auth: process.env.GITHUB_TOKEN });
    const owner = process.env.GITHUB_REPO_OWNER;
    const repo = process.env.GITHUB_REPO_NAME;

    const pr = await octokit.createPullRequest({
      owner: owner,
      repo: repo,
      title: `New submission for ${sub.assay.descriptor}`,
      body: `
      ${sub.submissionType} validation data for ${sub.assay.descriptor}

      ## Checklist

      - [ ] Check nomenclature of assay descriptors (assay.target, assay.targetSpecies, assay.type, assay.manufacturer, …)
      - [ ] Check accuracy and accessibility of assay manufacturer reference and url
      - [ ] Check contributor and author identity
      - [ ] Check matrices and metrics plausibility, compare with manufacturer instructions (reach out to contributor if manufacturer instructions are not available)
      - [ ] Check additional files, if any
      - [ ] For original submissions, check for previous publications
      - [ ] Preview submission (https://www.equine-assay-registry.org/preview)
      `,
      head: sub.id,
      base: "main",
      changes: [
        {
          files: filesToUpdate,
          commit: `Add validation data and files for ${sub.assay.descriptor}`
        }
      ]
    });

    if (sub.submissionType === "original") {
      await octokit.issues.addLabels({
        owner: owner,
        repo: repo,
        issue_number: pr.data.number,
        labels: ["doi"]
      });
    }
    return res.status(201).json({ success: true, pr_url: pr.data.html_url });
  } catch (error) {
    console.log(error);
    return res.status(500).json({ error: "Failed to create pull request" });
  }
}
