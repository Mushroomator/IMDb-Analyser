import { Grid } from "@chakra-ui/react"
import { Header } from '../components/Header';
import { Content } from '../components/Content';
import { Route, Routes } from 'react-router-dom';
import { ActorDetails } from './ActorDetails';
import { ActorList } from './ActorList';
import { Home } from './Home';
import { MovieList } from "./MovieList";

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
          <Route path="/movies" element={<MovieList/>} />
        </Route>
      </Routes>
    </Grid>
  );
}

export default App;
