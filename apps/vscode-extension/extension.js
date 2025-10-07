
const vscode = require('vscode');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

function activate(context) {
  let disposable = vscode.commands.registerCommand('codeatlas.ask', async function () {
    const question = await vscode.window.showInputBox({prompt: 'Ask CodeAtlas'});
    if (!question) return;
    const resp = await fetch('http://localhost:8080/v1/answer', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ question, k: 8 })
    }).then(r=>r.json());
    vscode.window.showInformationMessage(resp.answer.slice(0, 300) + '...');
  });
  context.subscriptions.push(disposable);
}
exports.activate = activate;
function deactivate() {}
module.exports = { activate, deactivate };
