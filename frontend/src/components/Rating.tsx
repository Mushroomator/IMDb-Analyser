import { Box, Text } from "@chakra-ui/react";
import { maxRating } from "../config";

export interface IRating {
    rating: number
}

export function Rating({ rating }: IRating) {
    return (
        <Box alignItems={"center"} justifyItems={"center"}>
            <Text display={"inline"} fontSize={"4xl"} fontWeight={"bold"}>
                {rating}
            </Text>
            <Text display={"inline"} fontSize={"md"} fontWeight={"light"}>
                /{maxRating}
            </Text>
        </Box>
    )
}