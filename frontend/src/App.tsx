import React, { useEffect, useState } from 'react';
import { Grid, GridItem, Progress } from "@chakra-ui/react"
import './App.css';
import { Header } from './components/Header';
import { Content } from './components/Content';
import { searchForStrInActorsAbout } from './searchUtils';
import ActorCard from './components/ActorCard';
import { IActorAbout, IActorsResponse } from './types';
import { NoDataAlert } from './components/NoDataAlert';
import { useFetch } from './hooks/useFetch';
import { Route, Routes } from 'react-router-dom';
import { GenericTable } from './components/GenericTable';
import { ActorDetails } from './components/ActorDetails';
import { ActorList } from './components/ActorList';
import { Home } from './components/Home';

function App() {
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
        "loading"
        "content"
        "footer"
        `
      ]}
      gridTemplateRows={[
        "75px 5px 1fr auto"
      ]}
      gridAutoColumns={[
        "1fr"
      ]}>
      <Header />
      <Routes>
        <Route path="/" element={<Content />}>
          <Route index element={<Home />} />
          <Route path="actors" element={<ActorList />} />
          <Route path="/actors/:actorId" element={<ActorDetails />} />

        </Route>
      </Routes>
    </Grid>
  );
}

export default App;
