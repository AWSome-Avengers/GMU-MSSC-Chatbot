# GMU-MSSC-Chatbot
GMU MSSC Chatbot

## PROBLEM DESCRIPTION
Traditional AI chatbots, while effective in handling standard queries, often struggle with providing accurate, contextually relevant, and up-to-date responses. Their limitations become apparent in complex conversation scenarios, where nuanced understanding and real-time information retrieval are essential.

The primary challenge is to overcome the limitations of conventional AI chatbots by enhancing their capabilities through the integration of a Large Language Model (LLM) and Retrieval-Augmented Generation (RAG). This integration aims to address the following specific issues:

1. Limited Contextual Understanding
1. Static Knowledge Base
1. Handling Complex Queries
1. Personalization Deficit
1. Scalability and Performance

## PROJECT GOALS
The overall project goal is to develop an AI chatbot that effectively integrates a LLM with RAG using AWS services to:

1. Enhance contextual understanding and maintain coherence over longer conversation threads.
1. Dynamically retrieve and incorporate up-to-date information from external sources in real-time.
1. Accurately understand and respond to complex, nuanced queries.
1. Offer personalized responses based on user interactions and preferences.
1. Maintain high performance and scalability for handling concurrent interactions across various domains.

## SOLTUION

1. The team created an [Amazon Kendra](https://aws.amazon.com/kendra/) index and used the [Web Crawler connector](https://docs.aws.amazon.com/kendra/latest/dg/data-source-v2-web-crawler.html) to index the [MSSC website](https://mssc.gmu.edu/) and all pages on gmu.edu linked from that website.
2. Next, we deployed the [QnABot solution](https://docs.aws.amazon.com/solutions/latest/qnabot-on-aws/solution-overview.html) from the [CloudFormation template](https://docs.aws.amazon.com/solutions/latest/qnabot-on-aws/step-1-launch-the-stack.html).  The chatbot was configured in collaboration with the MSSC partner as documented in our project report.
3. Finally, we deployed the [Lex Web Interface](https://github.com/aws-samples/aws-lex-web-ui) from another CloudFormation template.
