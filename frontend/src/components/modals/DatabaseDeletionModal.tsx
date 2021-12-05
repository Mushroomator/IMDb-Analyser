import { CheckCircleIcon, CheckIcon, CloseIcon, SmallCloseIcon } from "@chakra-ui/icons";
import { Alert, AlertDescription, AlertIcon, AlertTitle, Button, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay, Text } from "@chakra-ui/react";
import React, { useCallback, useState } from "react";
import { deleteAllDataFromDb } from "../../requests";
import { LoadingSpinner } from "../LoadingSpinner";

export type TModalClose = {
    onClose: () => void
}

export type TModalConfirmed = {
    onConfirmed: () => Promise<void>
}

export interface IModal {
    finalFocusRef: React.RefObject<any> | undefined
    isOpen: boolean
    onClose: () => void
}

type TDeletionStatus = "confirm" | "inProgress" | "success" | "failed";

// async function testFunc(result: boolean): Promise<boolean> {
//     return await new Promise(resolve => setTimeout(() => resolve(result), 5000));
// }


export function DatabaseDeletionModal({ finalFocusRef, isOpen, onClose }: IModal) {
    const [status, setStatus] = useState<TDeletionStatus>("confirm")

    const onDeletionConfirmed = async () => {
        setStatus("inProgress")
        const success = await deleteAllDataFromDb()
        if (success) {
            setStatus("success");
        }
        else {
            setStatus("failed");
        }
    }

    function onModalCancelled() {
        // reset status to initial state
        setStatus("confirm");
        // close modal
        onClose()
    }

    const modalConfig: Record<TDeletionStatus, React.ReactChild> = {
        confirm: <DatabaseDeletionConfirm onClose={onModalCancelled} onConfirmed={onDeletionConfirmed} />,
        inProgress: <DatabaseDeletionInProgress />,
        success: <DatabaseDeletionSuccess onClose={onModalCancelled} />,
        failed: <DatabaseDeletionFailed onClose={onModalCancelled} onConfirmed={onDeletionConfirmed}/>
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
            <ModalOverlay/>
            {modalConfig[status]}
        </Modal>
    )
}

function DatabaseDeletionConfirm({ onClose, onConfirmed: onDeletionConfirmed }: TModalClose & TModalConfirmed) {
    return (
        <ModalContent height={"220px"} minH={"220px"}>
            <ModalHeader>Delete all data?</ModalHeader>
            <ModalCloseButton />
            <ModalBody>
                <Text>I understand that the data is permanently deleted. Continue?</Text>
            </ModalBody>
            <ModalFooter>
                <Button colorScheme='blue' mr={3} onClick={() => onDeletionConfirmed()} leftIcon={<CheckIcon />}>
                    Yes, delete
                </Button>
                <Button variant='ghost' onClick={onClose} leftIcon={<SmallCloseIcon />}>Cancel</Button>
            </ModalFooter>
        </ModalContent>
    )
}

function DatabaseDeletionInProgress() {
    return (
        <ModalContent>
            <ModalHeader>Deletion in progress...</ModalHeader>
            <ModalBody>
                <LoadingSpinner height="200px"/>
            </ModalBody>
        </ModalContent>
    )
}

function DatabaseDeletionSuccess({ onClose }: TModalClose) {
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
                        Deletion successful!
                    </AlertTitle>
                    <AlertDescription maxWidth='sm'>
                        All data has successfully been deleted from the database.
                    </AlertDescription>
                </Alert>
            </ModalBody>
            <ModalFooter>
                <Button colorScheme='blue' mr={3} onClick={onClose} leftIcon={<SmallCloseIcon />}>
                    Close
                </Button>
            </ModalFooter>
        </ModalContent>
    )
}

function DatabaseDeletionFailed({ onClose, onConfirmed }: TModalClose & TModalConfirmed) {
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
                        Deletion failed!
                    </AlertTitle>
                    <AlertDescription maxWidth='sm'>
                        Data could not be deleted from the database. Retry?
                    </AlertDescription>
                </Alert>
            </ModalBody>
            <ModalFooter>
                <Button colorScheme='blue' mr={3} onClick={onConfirmed} leftIcon={<CheckIcon />}>
                    Yes, try again
                </Button>
                <Button variant='ghost' onClick={onClose} leftIcon={<SmallCloseIcon />}>Cancel</Button>
            </ModalFooter>
        </ModalContent>
    )
}