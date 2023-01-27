import CodeBlock from './CodeBlock.svelte';
import Code from './Code.svelte';

const codePlugin = {
    renderer: {
        pre: CodeBlock,
        code: Code,
    }
};

export default codePlugin;
