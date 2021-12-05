import { Box, Spinner } from "@chakra-ui/react";

export interface ILoadingSpinner {
    height?: string
}

export function LoadingSpinner({ height = "80vh" }: ILoadingSpinner) {
    return (
        <Box
            h={height}
            alignItems={"center"}
            justifyContent={"center"}
            display={"flex"}>
            <Spinner size={"xl"} color="blue.500" thickness="4px" />
        </Box>
    )
}