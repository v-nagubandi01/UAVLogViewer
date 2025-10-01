from unittest import result
import message_information 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
from uuid import uuid4

load_dotenv()


MESSAGE_TABLE_INFO = {k: v for k, v in vars(message_information).items() if not k.startswith("__")}

PERSIST_DIR = "message_selection_rag"
COLLECTION_NAME = "message_selection_rag1"
EMBEDDING_FUCTION = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",  
        task_type="RETRIEVAL_DOCUMENT",       
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )

def initialized_rag(collection_name = COLLECTION_NAME , persist_dir = PERSIST_DIR, embedding_function = EMBEDDING_FUCTION ):
    """ 
    Initialize and populate a RAG vector store if it has not been set up yet.

    Args:
        collection_name (str): The name of the Chroma collection to use.
        persist_dir (str): The directory path where the collection is persisted.
        embedding_function (Any): The embedding function used for document indexing.

    Behavior:
        - If the collection is empty:
            * Creates a Google Generative AI embedding function (Gemini).
            * Converts `MESSAGE_TABLE_INFO` into `Document` objects with
              `source` metadata.
            * Adds documents to the collection with generated UUIDs.
            * Prints a success message.
        - If the collection already contains documents:
            * Skips ingestion and prints a notice.
    
    """

    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embedding_function,
        persist_directory=persist_dir
    )

    if vector_store._collection.count() == 0:

        documents = []

        for message_type in MESSAGE_TABLE_INFO:
            document = Document(
                page_content = MESSAGE_TABLE_INFO[message_type],
                metadata = {'source':message_type}
            )
            documents.append(document)

        uuids = [str(uuid4()) for _ in range(len(documents))]

        vector_store.add_documents(documents=documents, ids=uuids)

        print("Successfully initialized rag and added documents")
    else:
        print("Collection already initialized. Skipping ingestion.")


def ensure_related_messages(string_list, list_of_groups):
    """
    For a list of string groups, ensures that if any member of a group is
    present in the list, all members of that group are included.
    
    Args:
        string_list: A list of strings to check.
        list_of_groups: A list where each item is a set of related strings.
        
    Returns:
        A new list with all group members included where applicable.
    """
    string_set = set(string_list)
    
    # Iterate through each group you want to check
    for group in list_of_groups:
        # Check if any string from the current group is in our set
        if not string_set.isdisjoint(group):
            # If yes, add ALL members of that group to the set
            string_set.update(group)
            
    # Return the result as a list
    return list(string_set)

    

# def query_rag(filter_messages:dict, query:str, k:int = 10):
#     """    
#     Query the RAG vector store and retrieve the most relevant results.

#     Args:
#         filter_messages (dict): A metadata filter to restrict search results.
#             Example: {"source": {"$in": ["GPS", "BARO", "POS"]}}
#         query (str): The natural language question to search against the stored documents.
#             Example: "What was the highest altitude reached?"
#         k (int): The number of top results to return. Defaults to 10.

#     Returns:
#         list: A list of (Document, score) tuples representing the most relevant matches.
    
#     """
#     vector_store = Chroma(
#         collection_name=COLLECTION_NAME,
#         embedding_function=EMBEDDING_FUCTION,
#         persist_directory=PERSIST_DIR,
#     )

#     retrieved_documents = vector_store.similarity_search_with_score(query, k=k, filter=filter_messages)

#     messages = []

#     for doc, score in retrieved_documents:
#         messages.append(doc.metadata['source'])

#     related_messages =  [
#         {'FTN1', 'FTN2'},
#         {'XKF1', 'XKF2', 'XKF3', 'XKF4', 'XKF5'},
#         {'XKV1', 'XKV2'}
#     ]

#     messages = ensure_related_messages(messages, related_messages)
    
#     return messages



def query_rag( query:str, k:int = 10):
    """    
    Query the RAG vector store and retrieve the most relevant results.

    Args:
        query (str): The natural language question to search against the stored documents.
            Example: "What was the highest altitude reached?"
        k (int): The number of top results to return. Defaults to 10.

    Returns:
        list: A list of (Document, score) tuples representing the most relevant matches.
    
    """
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=EMBEDDING_FUCTION,
        persist_directory=PERSIST_DIR,
    )

    retrieved_documents = vector_store.similarity_search_with_score(query, k=k)

    messages = []

    for doc, score in retrieved_documents:
        messages.append(doc.metadata['source'])

    related_messages =  [
        {'FTN1', 'FTN2'},
        {'XKF1', 'XKF2', 'XKF3', 'XKF4', 'XKF5'},
        {'XKV1', 'XKV2'}
    ]

    messages = ensure_related_messages(messages, related_messages)
    
    return messages


def test_rag() -> float:
    """
    Run test cases against query_rag and compute average recall.
    """

    #note the answers here don't mean that all of these messages have to necessarily be used just that they messages should be considered
    test_cases = [
        ("What was the highest altitude reached during the flight?", ["BARO", "GPS", "POS", "XKF5"]),
        ("How far did the drone travel from the home position?", ["GPS", "POS"]),
        ("What was the lowest height above ground level (HAGL)?", ["POS", "XKF5"]),
        ("Did the drone ever roll or pitch more than 45 degrees?", ["ATT", "AHR2"]),
        ("Was the yaw stable during the mission?", ["ATT", "AHR2", "XKF1", "XKF2", "XKF3"]),
        ("What was the lowest battery voltage during the flight?", ["BAT", "POWR"]),
        ("How much current did the motors draw at maximum throttle?", ["BAT", "MOTB", "RCOU"]),
        ("Did the GPS ever lose lock or drop below 6 satellites?", ["GPS", "GPA"]),
        ("Was the position estimate consistent between GPS and EKF?", ["GPS", "POS", "XKF2", "XKF3"]),
        ("Was altitude hold working properly?", ["PIDA", "PSCD", "CTUN", "POS"]),
        ("Were there large errors in pitch control?", ["PIDP", "ATT", "CTUN"]),
        ("Did the drone saturate the motors to maintain stability?", ["MOTB", "RCOU", "RATE"]),
        ("Were there any GPS glitches or EKF errors logged?", ["MSG", "ERR", "XKF3", "XKF4", "XKF5"]),
        ("Did the autopilot switch modes during flight?", ["MODE", "MSG"]),
        ("Were there any vibration warnings?", ["VIBE", "FTN", "FTN1", "FTN2", "IMU"]),
        ("Did the RC link quality drop at any point?", ["RCIN", "RCI2", "RAD"]),
        ("Were any mission commands uploaded/executed?", ["CMD", "MSG", "MODE"]),
        ("What parameters were changed during this log?", ["PARM"]),
        ("Did the barometer record rapid temperature changes?", ["BARO", "HEAT"]),
        ("Were there significant magnetometer disturbances?", ["MAG", "XKF2", "XKF3"]),
    ]

    recalls = []

    for question, expected in test_cases:
        predicted = set(query_rag(question))
        expected_set = set(expected)

        # recall = fraction of expected items that were retrieved
        intersection = predicted & expected_set
        recall = len(intersection) / len(expected_set)

        if recall < 1.0:  # only log when incomplete
            print(f"Q: {question}")
            print(f"\tExpected: {expected_set}")
            print(f"\tFound:    {intersection}")
            print(f"\tRecall:   {recall:.2f}")

        recalls.append(recall)

    return sum(recalls) / len(recalls)

# def test_rag(vector_store):
#     test_cases = [
#         ("What was the highest altitude reached during the flight?", ["BARO", "GPS", "POS", "XKF5"]),
#         ("How far did the drone travel from the home position?", ["GPS", "POS"]),
#         ("What was the lowest height above ground level (HAGL)?", ["POS", "XKF5"]),
#         ("Did the drone ever roll or pitch more than 45 degrees?", ["ATT", "AHR2"]),
#         ("Was the yaw stable during the mission?", ["ATT", "AHR2", "XKF1", "XKF2", "XKF3"]),
#         ("What was the lowest battery voltage during the flight?", ["BAT", "POWR"]),
#         ("How much current did the motors draw at maximum throttle?", ["BAT", "MOTB", "RCOU"]),
#         ("Did the GPS ever lose lock or drop below 6 satellites?", ["GPS", "GPA"]),
#         ("Was the position estimate consistent between GPS and EKF?", ["GPS", "POS", "XKF2", "XKF3"]),
#         ("Was altitude hold working properly?", ["PIDA", "PSCD", "CTUN", "POS"]),
#         ("Were there large errors in pitch control?", ["PIDP", "ATT", "CTUN"]),
#         ("Did the drone saturate the motors to maintain stability?", ["MOTB", "RCOU", "RATE"]),
#         ("Were there any GPS glitches or EKF errors logged?", ["MSG", "ERR", "XKF3", "XKF4", "XKF5"]),
#         ("Did the autopilot switch modes during flight?", ["MODE", "MSG"]),
#         ("Were there any vibration warnings?", ["VIBE", "FTN", "FTN1", "FTN2", "IMU"]),
#         ("Did the RC link quality drop at any point?", ["RCIN", "RCI2", "RAD"]),
#         ("Were any mission commands uploaded/executed?", ["CMD", "MSG", "MODE"]),
#         ("What parameters were changed during this log?", ["PARM"]),
#         ("Did the barometer record rapid temperature changes?", ["BARO", "HEAT"]),
#         ("Were there significant magnetometer disturbances?", ["MAG", "XKF2", "XKF3"]),
#     ]

#     results = []

#     for question, answer in test_cases:
#         predicted_answer = query_rag(question)


#     recall_score = []


#     for num, case in enumerate(test_cases):
        
#         pred_answer = results[num]
#         act_answer = case[1]
#         num_found = 0
#         not_found = 0

#         found = []

#         for msg in act_answer: 
#             if msg in pred_answer:
#                 num_found += 1
#                 found.append(msg)
#             else:
#                 not_found += 1


#         if num_found != len(act_answer):
#             print("total needed to find",len(act_answer),'\n\t', "num_found", num_found, "not found", not_found)
#             print('\t',case[0])
#             print("\t\t",'actual_answer' ,act_answer)
#             print("\t\t", 'retrieved_answer' ,found)
#             recall_score += num_found/len(act_answer)
#         else: 
#             recall_score += 1

    return sum(recall_score) / len(recall_score)




if __name__ == "__main__":
    initialize_rag(COLLECTION_NAME, PERSIST_DIR, EMBEDDING_FUCTION )
