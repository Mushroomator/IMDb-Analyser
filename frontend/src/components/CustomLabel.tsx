import { Text, TextProps } from "@chakra-ui/react"
import { ReactChild, ReactChildren } from "react"

interface ICustomLabel extends TextProps {
    children?: ReactChild | ReactChildren | ReactChild[] | ReactChildren[]
}

export function CustomLabel(props: ICustomLabel){
    return <Text {...props} _after={{ content: "':'" }} fontWeight={"black"}>{props.children}</Text>
}