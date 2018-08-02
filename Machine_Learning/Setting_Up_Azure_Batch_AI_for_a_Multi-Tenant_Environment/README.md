# [Setting Up Azure Batch AI for a Multi-Tenant Environment](https://medium.com/seismic-data-science/setting-up-azure-batch-ai-for-a-multi-tenant-environment-a51d86fb0ecb)
Author: [Orysya Stus](https://www.linkedin.com/in/orysyastus/)

Date: July 2018

### Goal

Set up and run Custom Toolkit training jobs in a multi-tenant environment using Azure Batch AI.

### In this blog, we will build out the Azure Batch AI infrastructure:
   1. Upload 30 day historical weather data into blob storage for each customer. Upload model for training, supporting scripts, and package requirements into file share. [Batch Step 1]
   2. Initialize Batch AI: Create the number of nodes per cluster, enable autoscaling of 0 nodes, and allow training jobs in parallel. [Batch Step 2]
   3. Run Azure Batch AI jobs using Custom Toolkit. Monitor job status and examine error/output logs for each job. Upload trained model for each customer into file share. [Batch Steps 3–5]
   4. Locally, predict upcoming 24 hour weather for each customer using the latest trained model downloaded from file share. [Batch Step 6]
