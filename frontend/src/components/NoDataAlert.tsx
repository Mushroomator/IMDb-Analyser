import { Alert, AlertIcon, AlertTitle, Box } from "@chakra-ui/react";

export function NoDataAlert() {
    return (
        <Alert
            status="info"
            variant="subtle"
            flexDirection="column"
            alignItems="center"
            justifyContent="center"
            textAlign="center"
            borderRadius={15}
            height="100px"
            flexGrow={1}
        >
            <AlertIcon boxSize="40px" mr={0} />
            <AlertTitle mt={4} mb={1} fontSize="lg">
                No data
            </AlertTitle>
        </Alert>
    )
}