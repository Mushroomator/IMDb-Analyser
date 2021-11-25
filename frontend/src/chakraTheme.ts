import { extendTheme, ThemeConfig } from "@chakra-ui/react"

const colorConfig : ThemeConfig = {
  initialColorMode: "light",
  useSystemColorMode: false
};

const theme = extendTheme({
  fonts: {
    heading: "Open Sans",
    body: "Open Sans",
  },
  config: colorConfig
})

export default extendTheme(theme);