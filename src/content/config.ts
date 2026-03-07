import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.string(),
    tags: z.array(z.string()),
    summary: z.string(),
    draft: z.boolean().default(true),
  }),
});

const notebooks = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.string(),
    tags: z.array(z.string()),
    techStack: z.array(z.string()),
    sector: z.enum(['industrial', 'commercial', 'utility', 'other']),
    summary: z.string(),
    keyFindings: z.array(z.string()),
    notebookFile: z.string(),
    renderedFile: z.string(),
    project: z.string(),
    projectTitle: z.string(),
    projectSummary: z.string(),
    order: z.number(),
  }),
});

export const collections = { blog, notebooks };
