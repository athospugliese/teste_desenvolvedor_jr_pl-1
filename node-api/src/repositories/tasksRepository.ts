import fs from "fs";

interface Task {
  id: number;
  text: string;
  summary: string | null;
  lang: string | null;
}

export class TasksRepository {
  private tasks: Task[] = [];
  private currentId: number = 1;
  private readonly filePath = "tasks.json";

  constructor() {
    this.loadTasks();
  }

  private saveTasks() {
    
    fs.writeFileSync(this.filePath, JSON.stringify(this.tasks, null, 2), "utf-8");
  }

  private loadTasks() {
    
    if (fs.existsSync(this.filePath)) {
      const data = fs.readFileSync(this.filePath, "utf-8");
      this.tasks = JSON.parse(data);
      if (this.tasks.length > 0) {
        this.currentId = Math.max(...this.tasks.map(task => task.id)) + 1; 
      }
    }
  }

  createTask(text: string, lang: string, summary: string): Task {
    const task: Task = {
      id: this.currentId++,
      text,
      summary,
      lang,
    };
    this.tasks.push(task);
    this.saveTasks();
    return task;
  }
      

  updateTask(id: number, summary: string, language: string): Task | null {
    const taskIndex = this.tasks.findIndex(t => t.id === id);
    if (taskIndex > -1) {
      this.tasks[taskIndex].summary = summary;
      this.tasks[taskIndex].lang = language;
      this.saveTasks();
      return this.tasks[taskIndex];
    }
    return null;
  }

  getTaskById(id: number): Task | null {
    return this.tasks.find(t => t.id === id) || null;
  }

  getAllTasks(): Task[] {
    return this.tasks;
  }

  deleteTask(id: number) {
    this.tasks = this.tasks.filter(item => item.id !== id);
    this.saveTasks();
  }
}