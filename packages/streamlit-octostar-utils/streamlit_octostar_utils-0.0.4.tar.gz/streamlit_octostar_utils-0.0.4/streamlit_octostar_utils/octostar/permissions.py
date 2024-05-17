import streamlit as st

from streamlit_octostar_research.desktop import get_open_workspace_ids
from octostar.utils.ontology import query_ontology
from octostar.utils.workspace.permissions import get_permissions, PermissionLevel

def get_workspaces():
    workspace_ids = get_open_workspace_ids()
    if not workspace_ids and st.session_state['input']['workspaces'] is not None:
        return
    if not workspace_ids:
        st.stop()
    workspace_ids = ", ".join(["'" + workspace_id + "'" for workspace_id in workspace_ids])
    workspaces = query_ontology.sync(f"SELECT `entity_label`, `os_entity_uid` FROM `dtimbr`.`os_workspace` WHERE `os_entity_uid` IN ({workspace_ids})")
    workspaces_permissions = get_permissions.sync([w['os_entity_uid'] for w in workspaces])
    workspaces = {workspace['os_entity_uid']: {**workspace, 'os_permission': workspaces_permissions.get(workspace['os_entity_uid'], PermissionLevel.NONE)} for workspace in workspaces}
    st.session_state['input']['workspaces'] = dict(filter(lambda x: x[1]['os_permission'] > PermissionLevel.NONE, workspaces.items()))
    st.rerun() # to make the above widgets not take space