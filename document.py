from __future__ import print_function

import json
import os.path
import socket
import time
import re

import jinja2
from cloudgenix import jd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from unipath import Path
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/documents", "https://www.googleapis.com/auth/drive"]
DOCUMENT_URL = "https://docs.google.com/document/d/"
batch_update_count = 0


class RevisionIdMismatch(Exception):
    pass


def jinja_to_data(template_path=None, template_str=None, jinja_out=None, **kwargs):
    """
    Generate the data from Jinja File and Data passed as KWARGS
    :param jinja_out: Output of the Jinja rendering before being json Loaded
    :param template_str:
    :param template_path: string or path of jinja template
    :param kwargs: Data for use in jinja template
    :return: rendered data as python object
    """
    template = str()
    if template_path:
        template = jinja2.Template(Path(template_path).read_file(), trim_blocks=True)
    if template_str:
        template = jinja2.Template(template_str, trim_blocks=True)
    data = template.render(**kwargs, j_dumps=j_dumps, j_loads=json.loads, TableCount=TableCount, re=re)
    if jinja_out:
        Path(jinja_out).write_file(data)
    try:
        return_obj = json.loads(data)
        return return_obj
    except Exception as e:
        Path('Jinja_render_issue.json').write_file(data)
        raise e


def j_dumps(raw_text):
    if isinstance(raw_text, (int, type(None))):
        raw_text = str(raw_text)
    json_txt = json.dumps(raw_text)
    return json_txt


class Document(object):
    d_out_path = Path('debug')
    debug = False

    default_style = {
        "table": {
            "header": {
                "textStyle": {
                    'bold': True
                }
            },
            "textStyle": {
                "fontSize": {
                    "magnitude": 10,
                    "unit": "PT"
                }
            }
        }
    }

    def __init__(self, doc_id=None, doc_name="NEW As Built Document", doc_copy_template=None, drive_folder_id=None):
        self.service = None
        self.doc_id = None
        self.drive_folder_id = drive_folder_id
        # Value to track where the Initial Copy of the document end, and where the new values start
        self.doc_obj_delta = 0
        self.doc_copy_template = doc_copy_template

        # Default Jinja Templates
        self.table_format_jinja = Path("templates/format_table.jinja2")
        self.insert_txt_jinja = Path("templates/insert_cell_values.jinja2")
        self.create_table_jinja = Path("templates/create_table.jinja2")
        self.paragraph_format_jinja = Path("templates/format_paragraph.jinja2")
        self.update_text_style_jinja = Path("templates/update_text_style.jinja2")

        self.__build_service()

        if doc_id:
            self.doc_id = doc_id
        else:
            self._create_doc(doc_name)

        self.update_doc_delta()

        # Print Document URL to CLI

    def get_url(self):
        return '{0}{1}'.format(DOCUMENT_URL, self.doc_id) + '/'

    def __build_service(self):
        """Shows basic usage of the Docs API.
        Prints the title of a sample document.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            # print("token.json was located")

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        # Interactor
        self.service = build('docs', 'v1', credentials=creds)
        self.drive_service = build('drive', 'v3', credentials=creds)

    def _create_doc(self, title):
        """
        Create Document using Jinja template for the Body
        :param title: Document Title
        :return: None
        """
        if self.doc_copy_template:
            drive_response = self.drive_service.files().copy(
                fileId=self.doc_copy_template,
                body={'name': title}
            ).execute()
            self.doc_id = drive_response.get('id')
        else:
            doc = self.service.documents().create(body={"title": title}).execute()
            self.doc_id = doc.get('documentId')
        if self.drive_folder_id is not None:
            self.move_doc(new_folder_id=self.drive_folder_id)
        print('Created document with title: {0}'.format(title))

    def move_doc(self, new_folder_id):
        file = self.drive_service.files().get(fileId=self.doc_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        file = self.drive_service.files().update(
            fileId=self.doc_id,
            addParents=new_folder_id,
            removeParents=previous_parents,
            fields='id, parents'
        ).execute()

    def update_doc_delta(self):
        """
        Update the Value of the Document where we should start Adding/where we added items. This list index is where the
        original document ended.
        :return:
        """
        self.doc_obj_delta = len(self.get_json_doc()["body"]["content"]) - 1

    def debug_print(self, str_print):
        """
        Print statement when debug  is enabled.
        :param str_print:
        :return:
        """
        if self.debug:
            print(str_print)

    def _batch_update(self, requests, max_requests=1000):
        """
        This has retrys
        Send API Requests to modify/add to google Docs
        :param requests:
        :param max_requests: maximum number of requests to send at a time.
        :return: None
        """
        max_try = 3
        self.debug_print(f'Total Number of Batch Update Requests: {len(requests)}')
        current_revision_id = self.get_json_doc()['revisionId']
        for n in range(len(requests) // max_requests + (len(requests) % max_requests > 0)):
            i = max_requests * n
            j = max_requests * (n + 1)
            for try_num in range(1, max_try + 1):
                start_str = f'[index {i}:{j} | Attempt: {try_num}]'
                start_time = time.time()
                try:
                    self.debug_print(f'{start_str} Batch Update started')
                    response = self.service.documents().batchUpdate(
                        documentId=self.doc_id,
                        body={
                            'requests': requests[i:j],
                            'writeControl': {'requiredRevisionId': current_revision_id}
                        }
                    ).execute()
                    self.debug_print(f'{start_str} Batch Update completed succesfully')
                    elaps_t = time.time() - start_time
                    self.debug_print("{} Time elapsed for batch update: {:.2f}s".format(start_str, elaps_t))
                    current_revision_id = response['writeControl']['requiredRevisionId']
                    break

                except socket.timeout:
                    print(60 * "*" + '\n' + f'{start_str} Batch Update failed (Socket.timeout)')
                    elaps_t = time.time() - start_time
                    print("{} Time elapsed for batch update: {:.2f}s".format(start_str, elaps_t), '\n' + 60 * "*")
                    print(60 * "*")
                    time.sleep(180)
                    t_revision_id = self.get_json_doc()['revisionId']
                    if t_revision_id != current_revision_id:
                        current_revision_id = t_revision_id
                        break
                    print('Revision ID is the same after 180 seconds, will try the changes again.')

                except Exception as e:
                    Path('batch_update_failed.json').write_file(json.dumps(requests[i:j], indent=4))
                    print(60 * "*" + "\n", f'{start_str} ERROR: Batch Update failed will RETRY!', "\n", e)
                    elaps_t = time.time() - start_time
                    print("{} Time elapsed for batch update: {:.2f}s".format(start_str, elaps_t), '\n' + 60 * "*")
                    time.sleep(60)
                    # re_rev_issue = "The\srequired\srevision\sID\s'\S+'\sdoes\snot\smatch\sthe\slatest\srevision\.\s*"
                    # re_search = re.compile(re_rev_issue)
                    # if bool(re_search.search(e.reason)):
                    #     print("Revision ID has changed.")
                    #     quit()

                    if try_num == max_try:
                        print('This was the final retry, Errors still occurred. exiting')
                        raise e

    def get_json_doc(self, doc_id=None):
        """
        return Google Doc as json.
        :return: Google Doc as json
        """
        if doc_id:
            return self.service.documents().get(documentId=doc_id).execute()
        return self.service.documents().get(documentId=self.doc_id).execute()

    def create_table(self, data, update=False):
        """
        Build out the requests list for creating table
        :param data: input from json document format
        :param update: push to batch update
        :return: requests for creating table
        """
        requests = jinja_to_data(self.create_table_jinja, data=data)
        if update:
            self._batch_update(requests)
        return requests

    def fill_and_format_table(self, gdoc_table, data, head_section, tail_section):
        format_requests = []
        # Build Caption Insert Request for head_caption
        if "head_caption" in data.keys():
            t_val = data['head_caption']['text']
            format_requests += jinja_to_data(self.insert_txt_jinja, text=t_val, gdocs_content=head_section)
        table_data = data["values"].copy()
        # Add in the Header Row in the front
        if "headers" in data.keys():
            table_data.insert(0, data["headers"])
        # Build Cell insert requests
        format_requests += self.fill_table(gdoc_table, table_data)
        # Build Formatting requests
        format_requests += jinja_to_data(
            self.table_format_jinja,
            table=gdoc_table,
            data=data,
            head_section=head_section,
            tail_section=tail_section,
            default_style=self.default_style
        )
        return format_requests

    def fill_table(self, gdoc_table, data):
        """
        Generates requests to fill table, may also include formatting depending on the jinja template
        :param gdoc_table: table dict from google docs
        :param data: data Needs to be a nxn matrix with Header included as a list
        :return: list of requests
        """
        requests = list()
        for i in range(len(data)):
            for j in range(len(data[i])):
                gdocs_content = gdoc_table["table"]["tableRows"][i]["tableCells"][j]["content"][0]
                # Only continue if entry is not None or Empty str
                if data[i][j] not in ['']:
                    text = data[i][j]
                    # need the json representation for str so that jinja parser reads accordingly, handled in template
                    requests += jinja_to_data(self.insert_txt_jinja, text=text, gdocs_content=gdocs_content)
        return requests

    def add_paragraph_at_end(self, text, update=True):
        requests = [{
            "insertText": {
                "text": text,
                "endOfSegmentLocation": {
                    "segmentId": ""
                }
            }
        }]
        if update:
            self._batch_update(requests)
        return requests

    def format_paragraph(self, **kwargs):
        requests = jinja_to_data(self.paragraph_format_jinja, **kwargs)
        return requests

    def update_text_style(self, **kwargs):
        requests = jinja_to_data(self.update_text_style_jinja, **kwargs)
        return requests

    def get_json_print(self, doc_id=None):
        """
        Print out the dict of the Document
        :param doc_id: Google Doc ID
        :return: None
        """
        result = self.get_json_doc(doc_id).get
        jd(result)

    def build_from_dict_data(self, doc_outline, max_requests):
        """
        Latest version of Document Build out function. Will add the texts and tables without cell values. After
        building out will call the document and use the index to format and fill in cell values.
        :param max_requests:
        :param doc_outline: json/dict outline of document
        :return: None
        """
        # Insert Tables and paragraphs
        build_requests = self.gen_build_requests(doc_outline)
        if self.debug:
            self.d_out_path.child('gdoc_build_batch_update_requests.json'). \
                write_file(json.dumps(build_requests, indent=4))
        self._batch_update(build_requests, max_requests)

        # Format the Document and insert Cell values.
        format_requests = self.gen_format_requests(doc_outline)
        if self.debug:
            self.d_out_path.child('gdoc_format_batch_update_requests.json'). \
                write_file(json.dumps(format_requests, indent=4))
        self._batch_update(format_requests, max_requests)

    def gen_build_requests(self, doc_outline):
        """
        Generates and combines all the requests for building out paragraphs and tables to one list.
        :param doc_outline: json/dict outline of document
        :return: requests for document build
        """
        build_requests = list()
        # generate the build requests.
        for line in doc_outline:
            if len(line) != 1:
                print("ERROR, Multiple Commands in the Named Style dictionary, top level should only have one key")
            for named_style, data in line.items():
                if named_style == "paragraph":
                    build_requests += self.add_paragraph_at_end(data["text"], False)
                elif named_style == "table":
                    table_data = data["values"].copy()
                    if "headers" in data.keys():
                        table_data.insert(0, data["headers"])
                    build_requests += self.create_table(table_data)
                elif named_style == 'image':
                    build_requests += self.add_image(data)
                elif named_style == 'page_break':
                    build_requests += self.add_page_break(data)
                else:
                    build_requests += self.add_paragraph_at_end(data["text"], False)
                build_requests += self.add_paragraph_at_end("\n", False)
        return build_requests

    def gen_format_requests(self, doc_outline):
        """
        Generates and combines all the requests for formatting the document to a single list.
        Will also include all the requests to add in a text to a cell within a table.
        List is REVERSED to update the file from end to start so we don't have to check start index.
        :param doc_outline: json/dict outline of document
        :return: requests for formatting, in reverse
        """
        # Crop out the Original copied Document Delta
        current_g_doc = self.get_json_doc()["body"]["content"][self.doc_obj_delta:]
        # jd(current_g_doc[0])
        # Tables have a "\n" before and after need to account for it using this delta
        index_delta = 0
        format_requests = list()
        for i in range(len(doc_outline)):
            for named_style, data in doc_outline[i].items():
                if named_style == "table":
                    # Need this to offset "\n" lines before table
                    index_delta += 1
                    format_requests += self.fill_and_format_table(
                        current_g_doc[i + index_delta],
                        data,
                        head_section=current_g_doc[i + index_delta - 1],
                        tail_section=current_g_doc[i + index_delta + 1]
                    )
                    # Need this to offset "\n" lines after table
                    index_delta += 1

                elif named_style not in ['paragraph', 'image']:
                    format_requests += self.format_paragraph(
                        named_style=named_style, paragraph_obj=current_g_doc[i + index_delta]
                    )
                if named_style not in ['image', 'table'] and 'textStyle' in data:
                    format_requests += self.update_text_style(
                        data=data, paragraph_obj=current_g_doc[i + index_delta]
                    )
        # Best practice to update in reverse
        format_requests.reverse()
        return format_requests

    def replace_value(self, key, new_value, match_case=True, batch_update=True):
        request_template = [{
            'replaceAllText': {
                'replaceText': new_value,
                'containsText': {
                    'text': key,
                    "matchCase": match_case
                }
            }
        }]
        if batch_update:
            self._batch_update(request_template)
        return request_template

    def replace_m_values(self, head='{{', tail='}}', batch_update=True, **kwargs):
        """
        Replace text in the document. Head and tail are to account for formatting tactics like Jinja.
        It is case sensitive
        :param batch_update: Do the Replacement now?
        :param head: default '{{' to be placed at beginning of search string.
        :param tail: default '}}' to be placed at end of search string.
        :param kwargs: values as argument or a passed dictionary
        :return:
        """
        requests = list()
        for key, val in kwargs.items():
            requests += self.replace_value(head + key + tail, val, batch_update=False)
        if batch_update:
            self._batch_update(requests)
        return requests

    def add_image(self, uri, update=False):
        requests = [{
            "insertInlineImage": {
                "uri": uri,
                "endOfSegmentLocation": {"segmentId": ""}
            }}]
        if update:
            self._batch_update(requests)
        return requests

    @staticmethod
    def add_page_break(data):
        requests = [{"insertPageBreak": {"endOfSegmentLocation": {"segmentId": ""}}}]
        return requests


class TableCount(object):
    def __init__(self, start_value=1):
        self.value = start_value

    def current(self):
        return self.value

    def next(self):
        v = self.value
        self.value += 1
        return v