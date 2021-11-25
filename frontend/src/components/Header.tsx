import { Grid, GridItem, Heading, HStack, Image } from "@chakra-ui/react";
import logo from "../assets/logo.png";
import { ISearchBar, SearchBar } from "./SearchBar";

export function Header({ searchStr, setSearchStr }: ISearchBar) {
    return (
        <GridItem position={"sticky"} top={0} zIndex={"sticky"} maxH={"100%"} h={"100%"} w={"100%"} bg={"white"} gridArea={"header"} borderBottom={"1px"} borderColor={"gray.200"}>
            <Grid
                w={"100%"}
                h={"100%"}
                gridTemplateAreas={
                    [
                        `"left middle middle"`,
                        `"left middle right"`
                ]}
                gridTemplateRows={"100%"}
                gridTemplateColumns={"20% 60% 20%"}
            >
                <GridItem
                    gridArea={"left"}
                >
                    <HStack h={"100%"} maxH={"100%"} alignItems={"center"} justifyContent={"start"} w={"100%"}>
                        <Image objectFit={"contain"} p={3} h={"100%"} maxW={"auto"} maxH={"100%"} src={logo} alt="IMDb Actor Database Logo" justifySelf={"start"} />
                        <Heading colorScheme={"blue"} display={["none", null, null, "block"]} size={"md"} justifyContent={"start"}>Actor Explorer</Heading>
                    </HStack>
                </GridItem>
                <GridItem
                    gridArea={"middle"}
                    w={"100%"}
                    h={"100%"}
                    display={"flex"}
                    alignItems={"center"}
                    justifyContent={"center"}>
                    <SearchBar setSearchStr={setSearchStr} searchStr={searchStr} />
                </GridItem>
            </Grid>


            {/* <HStack h={"100%"} maxH={"100%"} w={"100%"}> */}

            {/* </HStack> */}
        </GridItem>
    )
}