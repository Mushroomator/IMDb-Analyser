import { CheckIcon, SmallCloseIcon } from "@chakra-ui/icons";
import { Alert, AlertDescription, AlertIcon, AlertTitle, Button, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay, Progress, Text, VStack } from "@chakra-ui/react";
import React, { useEffect, useRef, useState } from "react";
import { getWebscrapingProgress, triggerWebscraping } from "../../requests";
import { Content } from "../Content";
import { LoadingSpinner } from "../LoadingSpinner";
import { IModal, TModalClose, TModalConfirmed } from "./DatabaseDeletionModal";

type TDeletionStatus = "confirm" | "inProgress" | "success" | "failed";

// async function testFunc(result: boolean): Promise<boolean> {
//     return await new Promise(resolve => setTimeout(() => resolve(result), 5000));
// }


export function WebscrapingModal({ finalFocusRef, isOpen, onClose }: IModal) {
    const [status, setStatus] = useState<TDeletionStatus>("confirm")
    const [ival, setIval] = useState<number>(0);

    const onWebscrapingConfirmed = async () => {
        const success = await triggerWebscraping()
        if (success) {
            setIval(success.monitorProgressVia.intervalInS);
            setStatus("inProgress");
        } else {
            setStatus("failed");
        }

    }

    function onModalCancelled() {
        // reset status to initial state
        setStatus("confirm");
        // close modal
        onClose()
    }

    function switchContent(): React.ReactChild {
        switch (status) {
            case "confirm":
                return <WebscrapingConfirm onClose={onModalCancelled} onConfirmed={onWebscrapingConfirmed} />
            case "inProgress":
                return <WebscrapingInProgress ivalInSec={ival} onFailed={() => setStatus("failed")} onSuccess={() => setStatus("success")} />
            case "success":
                return <WebscrapingSuccess onClose={onModalCancelled} />;
            case "failed":
                return <WebscrapingFailed onClose={onModalCancelled} onConfirmed={onWebscrapingConfirmed} />;
        }
    }



    return (
        <Modal
            closeOnOverlayClick={false}
            finalFocusRef={finalFocusRef}
            isCentered
            onClose={onClose}
            isOpen={isOpen}
            motionPreset='scale'
        >
            <ModalOverlay />
            {switchContent()}
        </Modal>
    )
}

function WebscrapingConfirm({ onClose, onConfirmed }: TModalClose & TModalConfirmed) {
    return (
        <ModalContent >
            <ModalHeader>Start webscraping?</ModalHeader>
            <ModalCloseButton />
            <ModalBody>
                <Text>All data will be deleted! The webscraping process will take about 10min. Continue?</Text>
                <Alert status='warning' my={4} borderRadius={"xl"}>
                    <AlertIcon />
                    Please make sure to wait ~15 minutes before requesting another run of the webscraper as it is possible to
                    reach the rate limit defined by imdb.com and therefore the IP address might get blocked and no/ some data might not get webscraped.
                </Alert>
            </ModalBody>
            <ModalFooter>
                <Button colorScheme='blue' mr={3} onClick={() => onConfirmed()} leftIcon={<CheckIcon />}>
                    Yes, webscrape
                </Button>
                <Button variant='ghost' onClick={onClose} leftIcon={<SmallCloseIcon />}>Cancel</Button>
            </ModalFooter>
        </ModalContent>
    )
}

interface IWebscrapingInProgress {
    ivalInSec: number
    onFailed: () => void
    onSuccess: () => void
}

function WebscrapingInProgress({ ivalInSec, onFailed, onSuccess }: IWebscrapingInProgress) {
    const [progress, setProgress] = useState<number>(0);

    useEffect(() => {
        async function processWebscrapingProgress() {
            const result = await getWebscrapingProgress()
            if (!result || result.status === "idle") {
                // some error occured or backend is not reachable
                onFailed()
            } else {
                if (result.progress === 100 && result.status === "finished") {
                    onSuccess()
                }
                else {
                    setProgress(result.progress)
                    setTimeout(processWebscrapingProgress, ivalInSec * 1000);
                }
            }
        }
        processWebscrapingProgress()
    }, [])

    return (
        <ModalContent>
            <ModalHeader>Webscraping in progress...</ModalHeader>
            <ModalBody>
                <VStack h={"200px"} minH={"200px"} justifyContent={"center"}>
                    <Progress value={progress} borderRadius={"xl"} w={"100%"} />
                    <Text>{`${progress}%`}</Text>
                </VStack>
            </ModalBody>
        </ModalContent>
    )
}

function WebscrapingSuccess({ onClose }: TModalClose) {
    return (
        <ModalContent>
            <ModalCloseButton />
            <ModalBody>
                <Alert
                    status='success'
                    variant='subtle'
                    bg={"transparent"}
                    flexDirection='column'
                    alignItems='center'
                    justifyContent='center'
                    textAlign='center'
                    height='200px'
                >
                    <AlertIcon boxSize='40px' mr={0} />
                    <AlertTitle mt={4} mb={1} fontSize='lg'>
                        Webscraping successful!
                    </AlertTitle>
                    <AlertDescription maxWidth='sm'>
                        All data has successfully been web scraped and inserted into the database.
                    </AlertDescription>
                </Alert>
            </ModalBody>
            <ModalFooter>
                <Button
                    variant='ghost'
                    onClick={() => {
                        onClose()
                        window.location.reload()
                    }}
                    leftIcon={<SmallCloseIcon />}>
                    Close
                </Button>
            </ModalFooter>
        </ModalContent>
    )
}

function WebscrapingFailed({ onClose, onConfirmed }: TModalClose & TModalConfirmed) {
    return (
        <ModalContent>
            <ModalCloseButton />
            <ModalBody>
                <Alert
                    status='error'
                    variant='subtle'
                    bg={"transparent"}
                    flexDirection='column'
                    alignItems='center'
                    justifyContent='center'
                    textAlign='center'
                    height='200px'
                    borderRadius={"xl"}
                >
                    <AlertIcon boxSize='40px' mr={0} />
                    <AlertTitle mt={4} mb={1} fontSize='lg'>
                        Webscraping failed!
                    </AlertTitle>
                    <AlertDescription maxWidth='sm'>
                        Data could not be webscraped and inserted into the database. Retry?
                    </AlertDescription>
                </Alert>
            </ModalBody>
            <ModalFooter>
                <Button colorScheme='blue' mr={3} onClick={onConfirmed} leftIcon={<CheckIcon />}>
                    Yes, try again
                </Button>
                <Button
                    variant='ghost'
                    onClick={() => {
                        onClose()
                    }}
                    leftIcon={<SmallCloseIcon />}>
                    Cancel
                </Button>
            </ModalFooter>
        </ModalContent>
    )
}