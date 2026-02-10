const apiBase = '';

async function fetchTodos(){
  const res = await fetch(`${apiBase}/todos`);
  const data = await res.json();
  return data.todos || [];
}

function el(tag, cls, text){
  const e = document.createElement(tag);
  if(cls) e.className = cls;
  if(text !== undefined) e.textContent = text;
  return e;
}

async function render(){
  const list = document.getElementById('todosList');
  list.innerHTML = '';
  const todos = await fetchTodos();

  if(todos.length === 0){
    const empty = el('div','todo', 'No todos yet. Add your first task!');
    list.appendChild(empty);
    return;
  }

  todos.forEach(todo => {
    const item = el('li','todo');
    const meta = el('div','meta');
    const title = el('h3', null, todo.title);
    if(todo.completed) title.parentElement?.classList?.add('completed');
    const desc = el('p', null, todo.description || '');
    meta.appendChild(title);
    if(todo.description) meta.appendChild(desc);

    const actions = el('div','actions');

    const toggle = el('button','btn', todo.completed ? 'Unmark' : 'Complete');
    toggle.addEventListener('click', async ()=>{
      await fetch(`${apiBase}/todos/${todo.id}`, {
        method:'PUT', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({completed: !todo.completed})
      });
      render();
    });

    const del = el('button','btn', 'Delete');
    del.addEventListener('click', async ()=>{
      if(!confirm('Delete this todo?')) return;
      await fetch(`${apiBase}/todos/${todo.id}`,{method:'DELETE'});
      render();
    });

    actions.appendChild(toggle);
    actions.appendChild(del);

    item.appendChild(meta);
    item.appendChild(actions);
    if(todo.completed) item.classList.add('completed');
    list.appendChild(item);
  });
}

document.addEventListener('DOMContentLoaded', ()=>{
  render();

  const form = document.getElementById('addForm') || document.getElementById('addBtn')?.closest('form');
  if(form){
    form.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const titleEl = document.getElementById('title');
      const descEl = document.getElementById('description');
      const title = titleEl.value.trim();
      if(!title) return;
      const description = descEl ? descEl.value.trim() : '';
      await fetch(`${apiBase}/todos`,{method:'POST',headers:{'Content-Type':'application/json'},body: JSON.stringify({title,description})});
      titleEl.value=''; if(descEl) descEl.value='';
      render();
    });
  }
});
