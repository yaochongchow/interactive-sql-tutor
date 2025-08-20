import Editor from 'react-simple-code-editor';
import { highlight, languages } from 'prismjs';
import 'prismjs/components/prism-sql.min.js';
import 'prismjs/themes/prism.css';

export default function SQLEditor({ value, onValueChange }) {
  return (
    <Editor
      placeholder='Type something...'
      value={value}
      onValueChange={onValueChange}
      highlight={(code) => highlight(code, languages.sql)}
      padding={10}
      style={{
        fontFamily: '"Fira code", "Fira Mono", monospace',
        fontSize: 16,
        'border-radius': '4px',
      }}
    />
  );
}
