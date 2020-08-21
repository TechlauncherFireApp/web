import React from "react";


export default class AssetRequestVehicle extends React.Component<any, any> {

    constructor(props: any) {
        super(props);
    }

    render() {
        return (
            this.props.match.params.id
        );
    }
}