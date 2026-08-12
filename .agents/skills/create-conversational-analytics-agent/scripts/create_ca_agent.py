"""
Script to create a Looker Conversational Analytics (CA) agent with custom instructions
and grant view access to the target embed group using Looker API raw endpoints.

Endpoints used:
1. POST /agents - Create agent with model/explore sources and custom prompt/instructions.
2. GET /content/{terms} - Search content by type 'agent' and term to locate content_id.
3. POST /content_metadata_access - Grant 'view' permission to the target user group.
"""

import os
import sys
import json
import dotenv
import looker_sdk

def create_ca_agent_and_grant_access(
    model_name: str,
    explore_name: str,
    agent_name: str,
    agent_desc: str,
    instructions: str,
    group_name_or_id: str
) -> dict:
    dotenv.load_dotenv('.env')
    sdk = looker_sdk.init40()

    # Step 1: POST /agents
    # Create agent with target model and explore sources and custom system instructions.
    agent_payload = {
        "name": agent_name,
        "description": agent_desc,
        "sources": [
            {
                "model": model_name,
                "explore": explore_name
            }
        ],
        "context": {
            "instructions": instructions
        }
    }
    
    res_agent = sdk.post("agents", structure=dict, body=agent_payload)
    agent = res_agent if isinstance(res_agent, dict) else {}
    agent_id = str(agent.get("id", ""))
    cm_id = str(agent.get("content_metadata_id", ""))

    # Step 2: GET /content/{terms}
    # Search content matching 'agent' to locate the content_id for the created agent.
    res_content = sdk.get("content/agent", structure=list)
    content_search_results = res_content if isinstance(res_content, list) else []
    located_content = None
    for item in content_search_results:
        if isinstance(item, dict):
            if item.get("type") == "agent" and (item.get("content_id") == agent_id or item.get("title") == agent_name):
                located_content = item
                break

    content_id = str(located_content.get("content_id", agent_id)) if isinstance(located_content, dict) else agent_id

    # Step 3: Resolve group ID if a group name was passed
    if not str(group_name_or_id).isdigit():
        groups = sdk.search_groups(name=group_name_or_id)
        if not groups:
            # Fallback search for any group containing the name
            all_groups = sdk.all_groups()
            matching_groups = [g for g in all_groups if g.name and group_name_or_id.lower() in g.name.lower()]
            if not matching_groups:
                raise ValueError(f"Group '{group_name_or_id}' could not be found.")
            group_id = str(matching_groups[0].id)
        else:
            group_id = str(groups[0].id)
    else:
        group_id = str(group_name_or_id)

    # Step 4: POST /content_metadata_access
    # Create content metadata access record with 'view' permission for the group.
    access_payload = {
        "content_metadata_id": cm_id,
        "group_id": group_id,
        "permission_type": "view"
    }

    res_access = sdk.post("content_metadata_access", structure=dict, body=access_payload)
    access_record = res_access if isinstance(res_access, dict) else {}

    return {
        "agent_id": agent_id,
        "content_id": content_id,
        "content_metadata_id": cm_id,
        "group_id": group_id,
        "access_record_id": str(access_record.get("id", "")),
        "agent": agent,
        "access_record": access_record
    }

if __name__ == "__main__":
    model = os.getenv("LOOKER_MODEL_NAME", "embed_demo")
    explore = os.getenv("LOOKER_EXPLORE_NAME", "shipping_logistics")
    agent_title = os.getenv("CA_AGENT_NAME", "Shipping Logistics CA Agent")
    agent_description = os.getenv("CA_AGENT_DESC", "Conversational analytics agent for shipping logistics")
    prompt_instructions = os.getenv(
        "CA_AGENT_PROMPT",
        "You are an expert shipping logistics data analyst. Answer questions about shipment status, delays, carrier performance, and delivery metrics accurately and concisely."
    )
    target_group = os.getenv("LOOKER_EMBED_GROUP", "Embed Demo Users")

    try:
        res = create_ca_agent_and_grant_access(
            model_name=model,
            explore_name=explore,
            agent_name=agent_title,
            agent_desc=agent_description,
            instructions=prompt_instructions,
            group_name_or_id=target_group
        )
        sys.stderr.write(f"Successfully created CA Agent and granted access:\n{json.dumps(res, indent=2)}\n")
    except Exception as err:
        sys.stderr.write(f"Error executing agent setup: {err}\n")
        sys.exit(1)
