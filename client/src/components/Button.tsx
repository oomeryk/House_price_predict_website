type Props = {
    text: string,
    onClick: () => void,
    color : "orange" | "green"
}

function Button(props : Props){
    const { text,onClick,color} = props ;

    let bgColor = "";
    let hoverBgColor = "";

    if(color === "orange"){
        bgColor = "bg-orange-600";
        hoverBgColor = "hover:bg-orange-800";
    }
    if(color === "green"){
        bgColor = "bg-green-600";
        hoverBgColor = "hover:bg-green-800";
    }

    return <button onClick={onClick} className={`w-60 p-2 ${bgColor} ${hoverBgColor} text-white rounded-md`}>{text}</button>
}

export default Button;