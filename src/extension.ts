'use strict';

import * as vscode from 'vscode';


const tokenTypes = ['string', 'number', 'function', 'keyword', 'macro', 'method'] as const;
const legend = new vscode.SemanticTokensLegend(<string[]><any>tokenTypes);
type TokenTypes = typeof tokenTypes[number];
const tokensNames: { [name: string]: TokenTypes } = {
	"str": "string",
	"num": "number",
	"int": "number",
	"float": "number",
	"bool": "macro",
	"map": "method",
}

const provider: vscode.DocumentSemanticTokensProvider = {
	provideDocumentSemanticTokens(
		document: vscode.TextDocument
	): vscode.ProviderResult<vscode.SemanticTokens>
	{
		const tokensBuilder = new vscode.SemanticTokensBuilder(legend);
		let curTypes: [TokenTypes, boolean][] = [];
		for (let i = 0; i < document.lineCount; i++)
		{
			const line = document.lineAt(i);
			const types = line.text.match(/(^[\w\t \-]*)(\((?:[\w\t \-\[\]]*)\))?[\t ]*([:=])/)?.[2];
			if (types)
			{
				curTypes = [];
				for (const type of types.matchAll(/[\w\t\-\[\]]+/g))
				{
					const v: RegExpMatchArray | null = type[0].match(/\w+/);
					if (v && v[0] in tokensNames)
						curTypes.push([tokensNames[v[0]], type[0].includes("[]") || type[0] == "map"])
					else
						curTypes.push(["keyword", type[0].includes("[]")])
				}
			}
			let vStart = line.text.indexOf("=") >= 0 ? line.text.indexOf("=") + 1 :
				(line.text.indexOf(":") >= 0 ? line.text.indexOf(":") + 1 : 0)
			const vEnd = line.text.indexOf(";") >= 0 ? line.text.indexOf(";") : line.text.length;
			let ti = 0;
			while (ti < curTypes.length)
			{
				const part = line.text.substring(vStart, vEnd);
				const word = part.match(/[^\s]+\s/)?.[0] || part;
				if (!word) break;
				const wordI = vStart + word.length;
				const t = curTypes[ti];
				if (t[1])
				{
					tokensBuilder.push(
						new vscode.Range(new vscode.Position(i, vStart), new vscode.Position(i, vEnd)),
						t[0]
					);
					break
				}
				else
				{
					tokensBuilder.push(
						new vscode.Range(new vscode.Position(i, vStart), new vscode.Position(i, wordI)),
						t[0]
					);
				}
				vStart = wordI;
				ti++;
			}
			if (line.text.indexOf(";") >= 0)
				curTypes = [];
		}
		const a = true;
		return tokensBuilder.build();
	}
};

const selector = { language: 'ultra_game_map', scheme: 'file' };

vscode.languages.registerDocumentSemanticTokensProvider(selector, provider, legend);
