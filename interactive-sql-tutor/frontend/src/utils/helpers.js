import { marked } from 'marked';

export const trim = (string, limit = 100) => {
  if (string.length <= limit) return string;
  return string.substring(0, limit) + '...';
};

export const isValidEmail = (email) => {
  const emailRegex = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/;
  return emailRegex.test(email);
};

export const getHeaders = (content_type = 'application/json') => {
  const token = localStorage.getItem('access-token');
  return {
    authorization: 'Bearer ' + token,
    'content-type': content_type,
  };
};

export const validateUser = (name, email, password, confirmedPassword) => {
  const nameRegex = /^[a-z A-Z]+$/;
  if (!name.trim()) return { ok: false, error: 'Name is missing!' };
  if (!nameRegex.test(name)) return { ok: false, error: 'Invalid name!' };
  if (!email.trim()) return { ok: false, error: 'Email is missing!' };
  if (!isValidEmail(email)) return { ok: false, error: 'Invalid email!' };
  if (!password.trim()) return { ok: false, error: 'Password is missing!' };
  if (password.length < 8)
    return { ok: false, error: 'Password must be at least 8 characters!' };
  if (password !== confirmedPassword)
    return { ok: false, error: "Passwords don't match!" };
  return { ok: true };
};

export const generatePromptFromProblem = (problem, hintResponses, hintStep) => {
  const { description, topic, tables, expected_output } = problem;

  let prompt = `
    You are solving a SQL problem. Here is the information:

    Problem:
    ${description}

    Topic:
    ${topic}

    Table format:
    ${JSON.stringify(tables, null, 2)}

    Expected Output:
    ${expected_output}

    Previous Hints:
    ${JSON.stringify(hintResponses, null, 2)}

  `;

  if (hintStep === 0) {
    prompt += `Now give your first hint. Focus on which SQL clauses (e.g., SELECT, JOIN, GROUP BY) the user should consider. Limit your answer to 30 words.`;
  } else if (hintStep === 1) {
    prompt += `Now give your next hint. Do not repeat earlier hints. Build upon them. Limit your answer to 30 words.`;
  } else {
    prompt += `Now provide the complete MySQL solution. Only reply with the SQL code.`;
  }

  return prompt.trim();
};

export const markdownToPlainText = (markdown) => {
  const html = marked(markdown);
  const text = html.replace(/<[^>]*>/g, '').trim();
  const textarea = document.createElement('textarea');
  textarea.innerHTML = text;
  return textarea.value;
};
