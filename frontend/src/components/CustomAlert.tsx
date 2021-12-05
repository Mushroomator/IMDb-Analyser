import { Alert, AlertDescription, AlertIcon, AlertTitle, Box } from "@chakra-ui/react";

export interface IDataError {
    status: "success" | "info" | "warning" | "error" | undefined
    alertTitle?: string
    alertDesc?: string
    height?: string
}

export function CustomAlert({ status, alertTitle, alertDesc, height = '200px' }: IDataError) {
    return (
        <Box
            h={height}
            w={"100%"}
            alignItems={"center"}
            justifyContent={"center"}
            display={"flex"}>
            <Alert
                status={status}
                variant='subtle'
                borderRadius={"xl"}
                flexDirection='column'
                alignItems='center'
                justifyContent='center'
                textAlign='center'
                height={"100%"}
            >
                <AlertIcon boxSize='40px' mr={0} />
                {alertTitle &&
                    <AlertTitle mt={4} mb={1} fontSize='lg'>
                        {alertTitle}
                    </AlertTitle>
                }
                {alertDesc &&
                    <AlertDescription maxWidth='sm'>
                        {alertDesc}
                    </AlertDescription>
                }
            </Alert>
        </Box>
    )
}