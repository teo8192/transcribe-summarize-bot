from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

import config

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(config.TEXT_ANALYTICS_KEY)
    text_analytics_client = TextAnalyticsClient(
            endpoint=config.TEXT_ANALYTICS_ENDPOINT, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Example method for summarizing text
def summarize_text(document: list[str]):
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import (
        TextAnalyticsClient,
        ExtractSummaryAction
    )

    poller = client.begin_analyze_actions(
        document,
        actions=[
            ExtractSummaryAction(max_sentence_count=4)
        ],
    )

    summaries = []

    document_results = poller.result()
    for result in document_results:
        extract_summary_result = result[0]  # first document, first result
        if extract_summary_result.is_error:
            raise Exception("Error with code '{}' and message '{}'".format(
                extract_summary_result.code, extract_summary_result.message
            ))
        else:
            summaries.append(" ".join([sentence.text for sentence in extract_summary_result.sentences]))

    return summaries

if __name__ == "__main__":
    with open("./recordings/213759644072542208-2023-03-24_21-39-24.txt", "r") as f:
        text = list(map(lambda x : x.strip("\n"), f.readlines()))
    print("Text: ", text)
    summary = summarize_text(["\n".join(text)])
    print("Summary: ", summary)
