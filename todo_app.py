import argparse
import json
import os
import sys
from datetime import datetime, timezone


TODO_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todos.json")


def load_todos() -> list[dict]:
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_todos(todos: list[dict]) -> None:
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2, ensure_ascii=False)


def next_id(todos: list[dict]) -> int:
    return max((t["id"] for t in todos), default=0) + 1


def cmd_add(args: argparse.Namespace) -> None:
    todos = load_todos()
    todo = {
        "id": next_id(todos),
        "title": " ".join(args.title),
        "completed": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    todos.append(todo)
    save_todos(todos)
    print(f"Task adaugat: [{todo['id']}] {todo['title']}")


def cmd_list(args: argparse.Namespace) -> None:
    todos = load_todos()
    if not todos:
        print("Lista de task-uri este goala.")
        return

    if args.all:
        items = todos
    else:
        items = [t for t in todos if not t["completed"]]
        if not items:
            print("Toate task-urile sunt finalizate! Folositi --all pentru a le vedea pe toate.")
            return

    print(f"\nTask-uri ({'toate' if args.all else 'nefinalizate'}):")
    print("=" * 40)
    for t in items:
        status = "\u2713" if t["completed"] else " "
        print(f"  [{status}] {t['id']:>3}. {t['title']}")
    print()


def cmd_done(args: argparse.Namespace) -> None:
    todos = load_todos()
    for todo in todos:
        if todo["id"] == args.id:
            todo["completed"] = True
            save_todos(todos)
            print(f"Task-ul [{args.id}] a fost marcat ca finalizat.")
            return
    print(f"Task-ul cu ID-ul {args.id} nu a fost gasit.")
    sys.exit(1)


def cmd_delete(args: argparse.Namespace) -> None:
    todos = load_todos()
    for i, todo in enumerate(todos):
        if todo["id"] == args.id:
            removed = todos.pop(i)
            save_todos(todos)
            print(f"Task-ul [{removed['id']}] '{removed['title']}' a fost sters.")
            return
    print(f"Task-ul cu ID-ul {args.id} nu a fost gasit.")
    sys.exit(1)


def cmd_clear(args: argparse.Namespace) -> None:
    save_todos([])
    print("Toate task-urile au fost sterse.")


def main():
    parser = argparse.ArgumentParser(description="Aplicatie TODO - CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Adauga un task nou")
    p_add.add_argument("title", nargs="+", help="Titlul task-ului")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="Listeaza task-urile")
    p_list.add_argument("--all", action="store_true", help="Arata si task-urile finalizate")
    p_list.set_defaults(func=cmd_list)

    p_done = sub.add_parser("done", help="Marcheaza un task ca finalizat")
    p_done.add_argument("id", type=int, help="ID-ul task-ului")
    p_done.set_defaults(func=cmd_done)

    p_del = sub.add_parser("delete", help="Sterge un task")
    p_del.add_argument("id", type=int, help="ID-ul task-ului")
    p_del.set_defaults(func=cmd_delete)

    p_clr = sub.add_parser("clear", help="Sterge toate task-urile")
    p_clr.set_defaults(func=cmd_clear)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
