import { Router, Request, Response } from "express";
import { TasksRepository } from "../repositories/tasksRepository";
import axios from "axios";

const router = Router();
const tasksRepository = new TasksRepository();

// POST: Cria uma tarefa e solicita resumo ao serviço Python
router.post("/", async (req: Request, res: Response) => {
  try {
    const { text, lang } = req.body;
    if (!text || !lang) {
      return res.status(400).json({ error: 'Campos "text" e "lang" são obrigatórios.' });
    }

    // Chamar a API de resumo
    const response = await axios.post("http://localhost:8000/summarize", { text, lang });
    const summary = response.data.summary;

    // Criar a tarefa no repositório
    const task = tasksRepository.createTask(text, lang, summary);
    return res.status(201).json(task);
  } catch (error) {
    console.error("Erro ao criar tarefa:", error);
    return res.status(500).json({ error: "Ocorreu um erro ao criar a tarefa." });
  }
});

// GET: Lista todas as tarefas
router.get("/", (req, res) => {
  const tasks = tasksRepository.getAllTasks();
  return res.json(tasks);
});

// GET: Lista uma tarefa específica
router.get("/:id", (req, res) => {
  const taskId = Number(req.params.id);
  const task = tasksRepository.getTaskById(taskId);
  if (!task) {
    return res.status(404).json({ error: "Tarefa não encontrada." });
  }
  return res.json(task);
});


export default router;
