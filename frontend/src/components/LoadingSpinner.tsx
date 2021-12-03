import { Box, Spinner } from "@chakra-ui/react";

export function LoadingSpinner() {
    return <Box
        h={"80vh"}
        alignItems={"center"}
        justifyContent={"center"}
        display={"flex"}>
        <Spinner size={"xl"} color="blue.500" thickness="4px" />
    </Box>;
}