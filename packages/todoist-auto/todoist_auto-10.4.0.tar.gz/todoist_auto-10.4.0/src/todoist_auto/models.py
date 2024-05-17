from mtok import get_token

class Var :
    url = 'url'
    jsn = 'json'
    indnt = 'INDENT'
    srt = 'sort'
    sec = 'section'
    secn = 'secn'
    secmt = 'sec_max_time'
    pri = 'PRIORITY'
    cnt = 'CONTENT'
    ty = "TYPE"
    sec_id = 'sec_id'
    par_id = 'par_id'
    labels = 'labels'
    excl = 'Exclude'
    rm_sec = 'remove_section'
    id = 'ID'
    dsc = 'Description'

VAR = Var()

class TodoistTask :
    assignee_id = 'assignee_id'
    assigner_id = 'assigner_id'
    comment_count = 'comment_count'
    is_completed = 'is_completed'
    content = 'content'
    created_at = 'created_at'
    creator_id = 'creator_id'
    description = 'description'
    due = 'due'
    id = 'id'
    labels = 'labels'
    order = 'order'
    parent_id = 'parent_id'
    priority = 'priority'
    project_id = 'project_id'
    section_id = 'section_id'
    url = 'url'

TODOISTTASK = TodoistTask()

class TodoistSection :
    id = 'id'
    name = 'name'
    order = 'order'
    project_id = 'project_id'

TODOISTSECTION = TodoistSection()

class TodoistProject :
    color = 'color'
    comment_count = 'comment_count'
    id = 'id'
    is_favorite = 'is_favorite'
    is_inbox_project = 'is_inbox_project'
    is_shared = 'is_shared'
    is_team_inbox = 'is_team_inbox'
    name = 'name'
    order = 'order'
    parent_id = 'parent_id'
    url = 'url'
    view_style = 'view_style'

TODOISTPROJECT = TodoistProject()

class Types :
    tsk = 'task'
    sec = 'section'

TYPES = Types()

class Notion :
    tok = get_token('Notion_imahdimirgmail')
    db_id = get_token('Notion_Routine_DB_ID')
    db_url = f'https://api.notion.com/v1/databases/{db_id}/query'
    pg_url = 'https://api.notion.com/v1/pages/'
    hdrs = {
            'Authorization'  : f'Bearer {tok}' ,
            'Notion-Version' : '2022-06-28' ,
            }

NOTION = Notion()

class Todoist :
    tok = get_token('Todoist')
    hdrs = {
            'Authorization' : f'Bearer {tok}'
            }
    routine_proj_id = '2312505898'

TODOIST = Todoist()
