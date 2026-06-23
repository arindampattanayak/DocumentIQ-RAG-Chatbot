import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

function getErrorMessage(error) {
  if (error.response?.data?.detail) {
    if (typeof error.response.data.detail === "string") {
      return error.response.data.detail;
    }
    return JSON.stringify(error.response.data.detail);
  }
  return error.message || "Unknown error";
}

export async function signup(payload) {
  try {
    const res = await api.post("/auth/signup", payload);
    return res.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function login(payload) {
  try {
    const res = await api.post("/auth/login", payload);
    return res.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function logout() {
  try {
    const res = await api.post("/auth/logout");
    return res.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function me() {
  try {
    const res = await api.get("/auth/me");
    return res.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function uploadDocument(file) {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const res = await api.post("/upload-doc", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return res.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function listDocuments() {
  try {
    const res = await api.get("/list-docs");
    return res.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function deleteDocument(fileId) {
  try {
    const res = await api.delete("/delete-doc", {
      params: { file_id: fileId },
    });
    return res.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function sendChat({ question, session_id = null, model = "gemini-2.5-flash" }) {
  try {
    const payload = { question, model };
    if (session_id) payload.session_id = session_id;

    const res = await api.post("/chat", payload);
    return res.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function getHistory() {
  try {
    const res = await api.get("/history");
    return res.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}

export async function getSessions() {
  try {
    const res = await api.get("/sessions");
    return res.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
}