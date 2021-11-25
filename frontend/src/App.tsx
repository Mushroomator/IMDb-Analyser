import React, { useState } from 'react';
import { Grid, useColorMode } from "@chakra-ui/react"
import './App.css';
import { Header } from './components/Header';
import { Content } from './components/Content';
import { testdata } from './test';
import { searchForStrInActors } from './searchUtils';
import ActorCard from './components/ActorCard';

function App() {
  const [searchStr, setSearchStr] = useState<string>("");

  console.log("before search", testdata)
  const searchResults = searchForStrInActors(testdata, searchStr.toLowerCase());
  console.log("after search", testdata)
  const content = searchResults.map((actor, idx) => (
    <ActorCard key={idx} actor={actor}/>
  ));

  return (
    <Grid 
      p="0" 
      m="0" 
      w="100%"
      minH={"100vh"} 
      h="100%"
      bg={"gray.50"}
      templateAreas={[
        `
        "header"
        "content"
        "footer"
        `
      ]}
      gridTemplateRows={[
        "75px 1fr auto"
      ]}
      gridAutoColumns={[
        "1fr"
      ]}>
      <Header  searchStr={searchStr} setSearchStr={setSearchStr}/>
      <Content children={content}/>
    </Grid>
  );
}

export default App;
