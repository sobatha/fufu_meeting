// rollup.config.js
import postcss from 'rollup-plugin-postcss'
// import preprocess from 'svelte-preprocess'
import sveltePreprocess from 'svelte-preprocess';

const preprocess = sveltePreprocess({
  scss: {
    includePaths: ['src'],
  },
  postcss: {
    plugins: [require('autoprefixer')],
  },
 });

export default {
  // ...
  // client: {
    plugins: [
      svelte({
        // ...
        preprocess: sveltePreprocess()
      }),   
      // postcss(),
    ]
  // },
  // server: {
  //   plugins: [
  //     svelte({
  //       // ...
  //       preprocess
  //     }),   
  //     // postcss(),
  //   ]
  // }
}