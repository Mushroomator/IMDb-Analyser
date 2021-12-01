import React from 'react';
import ReactDOM from 'react-dom';
import { ChakraProvider, ColorModeScript } from "@chakra-ui/react"
import './index.css';
import App from './App';
import "@fontsource/open-sans"
import theme from "./chakraTheme";
import { BrowserRouter } from 'react-router-dom';

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
      <ChakraProvider theme={theme}>
        <ColorModeScript initialColorMode={theme.config.initialColorMode} />
        <App />
      </ChakraProvider>
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);
