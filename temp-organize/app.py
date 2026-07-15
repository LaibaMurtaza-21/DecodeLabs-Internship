import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date

st.set_page_config(page_title="Smart Task Manager", layout="wide")

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task.get("id", 0) for task in tasks) + 1

def normalize_task(task):
    task.setdefault("description", "")
    task.setdefault("priority", "Medium")
    task.setdefault("status", "Pending")
    task.setdefault("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    task.setdefault("updated_at", "")
    task.setdefault("completed_at", "")
    return task

def overdue_count(tasks):
    count = 0
    for task in tasks:
        try:
            if task["status"] == "Pending" and date.fromisoformat(task["due_date"]) < date.today():
                count += 1
        except:
            pass
    return count

def tasks_df(tasks):
    if not tasks:
        return pd.DataFrame(columns=["id", "title", "description", "priority", "due_date", "status", "created_at", "updated_at", "completed_at"])
    return pd.DataFrame([normalize_task(task.copy()) for task in tasks])

def apply_filters(tasks, search_text, status_filter):
    result = []
    search_text = search_text.lower().strip()

    for task in tasks:
        task = normalize_task(task.copy())
        title_match = search_text in task["title"].lower()

        status_match = False
        if status_filter == "All":
            status_match = True
        elif status_filter == "Pending":
            status_match = task["status"] == "Pending"
        elif status_filter == "Completed":
            status_match = task["status"] == "Completed"
        elif status_filter == "High Priority":
            status_match = task["priority"] == "High"
        elif status_filter == "Overdue":
            try:
                status_match = task["status"] == "Pending" and date.fromisoformat(task["due_date"]) < date.today()
            except:
                status_match = False

        if title_match and status_match:
            result.append(task)

    return result

def mark_completed(task, tasks):
    for t in tasks:
        if t["id"] == task["id"]:
            t["status"] = "Completed"
            t["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            t["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    save_tasks(tasks)

def delete_task(task, tasks):
    tasks[:] = [t for t in tasks if t["id"] != task["id"]]
    save_tasks(tasks)

def update_task(task_id, tasks, title, description, priority, due_date):
    for t in tasks:
        if t["id"] == task_id:
            t["title"] = title
            t["description"] = description
            t["priority"] = priority
            t["due_date"] = str(due_date)
            t["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    save_tasks(tasks)

def add_task(tasks, title, description, priority, due_date):
    task = {
        "id": get_next_id(tasks),
        "title": title.strip(),
        "description": description.strip(),
        "priority": priority,
        "due_date": str(due_date),
        "status": "Pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": "",
        "completed_at": ""
    }
    tasks.append(task)
    save_tasks(tasks)

tasks = load_tasks()
tasks = [normalize_task(t) for t in tasks]

st.title("Smart Task Manager")

menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Add Task", "Task Manager", "Analytics", "Export Report", "About"]
)

total = len(tasks)
completed = len([t for t in tasks if t["status"] == "Completed"])
pending = total - completed
overdue = overdue_count(tasks)
progress = completed / total if total > 0 else 0

st.sidebar.markdown("### Quick Stats")
st.sidebar.metric("Total", total)
st.sidebar.metric("Completed", completed)
st.sidebar.metric("Pending", pending)
st.sidebar.metric("Overdue", overdue)

if menu == "Dashboard":
    st.subheader("Dashboard")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Tasks", total)
    c2.metric("Completed", completed)
    c3.metric("Pending", pending)
    c4.metric("Overdue", overdue)

    st.subheader("Progress")
    st.progress(progress)
    st.write(f"Completion Rate: {progress:.0%}")

    if total > 0:
        df = tasks_df(tasks)
        st.subheader("Due Date Overview")
        try:
            due_counts = df["due_date"].value_counts().sort_index()
            st.bar_chart(due_counts)
        except:
            st.info("No valid due date data available.")

elif menu == "Add Task":
    st.subheader("Add New Task")

    with st.form("add_task_form", clear_on_submit=True):
        title = st.text_input("Task Title")
        description = st.text_area("Description")
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        due_date = st.date_input("Due Date")
        submitted = st.form_submit_button("Add Task")

    if submitted:
        if title.strip() == "":
            st.error("Task title is required.")
        elif any(t["title"].strip().lower() == title.strip().lower() for t in tasks):
            st.error("A task with this title already exists.")
        else:
            add_task(tasks, title, description, priority, due_date)
            st.success("Task added successfully.")
            st.rerun()

elif menu == "Task Manager":
    st.subheader("Manage Tasks")

    if len(tasks) == 0:
        st.info("No tasks available.")
    else:
        search = st.text_input("Search Task")
        status_filter = st.selectbox("Filter", ["All", "Pending", "Completed", "High Priority", "Overdue"])

        filtered_tasks = apply_filters(tasks, search, status_filter)

        if not filtered_tasks:
            st.warning("No matching tasks found.")
        else:
            for task in filtered_tasks:
                with st.expander(f"{task['id']} - {task['title']}"):
                    st.write("Description:", task["description"])
                    st.write("Priority:", task["priority"])
                    st.write("Due Date:", task["due_date"])
                    st.write("Status:", task["status"])
                    st.write("Created At:", task["created_at"])
                    st.write("Updated At:", task["updated_at"] if task["updated_at"] else "N/A")
                    st.write("Completed At:", task["completed_at"] if task["completed_at"] else "N/A")

                    action_col1, action_col2, action_col3 = st.columns(3)

                    with action_col1:
                        if task["status"] == "Pending":
                            if st.button(f"Complete {task['id']}", key=f"complete_{task['id']}"):
                                mark_completed(task, tasks)
                                st.success("Task marked as completed.")
                                st.rerun()

                    with action_col2:
                        edit_key = f"edit_{task['id']}"
                        if st.button(f"Edit {task['id']}", key=edit_key):
                            st.session_state[f"editing_{task['id']}"] = True

                    with action_col3:
                        if st.button(f"Delete {task['id']}", key=f"delete_{task['id']}"):
                            delete_task(task, tasks)
                            st.success("Task deleted successfully.")
                            st.rerun()

                    if st.session_state.get(f"editing_{task['id']}", False):
                        st.markdown("### Edit Task")
                        with st.form(f"edit_form_{task['id']}"):
                            new_title = st.text_input("Title", value=task["title"])
                            new_description = st.text_area("Description", value=task["description"])
                            new_priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(task["priority"]))
                            # protect against invalid due_date formats
                            try:
                                init_due = date.fromisoformat(task["due_date"])
                            except:
                                init_due = date.today()
                            new_due_date = st.date_input("Due Date", value=init_due)
                            save_edit = st.form_submit_button("Save Changes")

                        if save_edit:
                            if new_title.strip() == "":
                                st.error("Task title cannot be empty.")
                            else:
                                duplicate = any(
                                    t["id"] != task["id"] and t["title"].strip().lower() == new_title.strip().lower()
                                    for t in tasks
                                )
                                if duplicate:
                                    st.error("Another task with this title already exists.")
                                else:
                                    update_task(task["id"], tasks, new_title, new_description, new_priority, new_due_date)
                                    st.session_state[f"editing_{task['id']}"] = False
                                    st.success("Task updated successfully.")
                                    st.rerun()

elif menu == "Analytics":
    st.subheader("Analytics")

    if len(tasks) == 0:
        st.info("No data available.")
    else:
        df = tasks_df(tasks)

        st.subheader("Tasks by Priority")
        priority_counts = df["priority"].value_counts()
        st.bar_chart(priority_counts)

        st.subheader("Tasks by Status")
        status_counts = df["status"].value_counts()
        st.bar_chart(status_counts)

        st.subheader("Overdue vs On Time")
        overdue_tasks = overdue_count(tasks)
        on_time_tasks = max(0, total - overdue_tasks)
        chart_df = pd.DataFrame({
            "Category": ["Overdue", "On Time"],
            "Count": [overdue_tasks, on_time_tasks]
        }).set_index("Category")
        st.bar_chart(chart_df)

elif menu == "Export Report":
    st.subheader("Download Report")

    if len(tasks) == 0:
        st.info("No tasks available.")
    else:
        df = tasks_df(tasks)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False)
        filename = f"tasks_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        st.download_button(
            "Download CSV Report",
            csv,
            filename,
            "text/csv"
        )

elif menu == "About":
    st.subheader("Project Information")
    st.write("""
    Smart Task Manager

    Technologies:
    - Python
    - Streamlit
    - Pandas
    - JSON

    Features:
    - Add Task
    - View Tasks
    - Complete Task
    - Edit Task
    - Delete Task
    - Search Tasks
    - Analytics
    - Export Report
    - Data Persistence
    """)