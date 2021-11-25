import React from 'react';
import ReactDOM from 'react-dom';
import { ChakraProvider, ColorModeScript, extendTheme } from "@chakra-ui/react"
import './index.css';
import App from './App';
import "@fontsource/open-sans"
import theme from "./chakraTheme";

ReactDOM.render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <ColorModeScript initialColorMode={theme.config.initialColorMode} />
      <App />
    </ChakraProvider>
  </React.StrictMode>,
  document.getElementById('root')
);
