{
  "metadataSchema": {
    "fields": [
      {
        "name": "Parcel ID",
        "type": "String",
        "description": "A unique identifier for each parcel (e.g., P12345678).",
        "required": true
      },
      {
        "name": "Sender Name",
        "type": "String",
        "description": "The name of the person or company sending the parcel.",
        "required": true
      },
      {
        "name": "Receiver Name",
        "type": "String",
        "description": "The name of the person or company receiving the parcel.",
        "required": true
      },
      {
        "name": "Pickup Address",
        "type": "String",
        "description": "The address from where the parcel is picked up.",
        "required": true
      },
      {
        "name": "Delivery Address",
        "type": "String",
        "description": "The destination address for the parcel.",
        "required": true
      },
      {
        "name": "Parcel Weight (kg)",
        "type": "Float",
        "description": "The weight of the parcel in kilograms.",
        "required": true
      },
      {
        "name": "Parcel Dimensions (cm)",
        "type": "String",
        "description": "The dimensions (length, width, height) of the parcel in centimeters.",
        "required": true
      },
      {
        "name": "Shipping Method",
        "type": "String",
        "description": "The type of shipping (e.g., standard, express, overnight).",
        "required": true
      },
      {
        "name": "Status",
        "type": "String",
        "description": "Current status of the parcel (e.g., pending, in transit, delivered, returned).",
        "required": true
      },
      {
        "name": "Date of Pickup",
        "type": "Date",
        "description": "The date when the parcel was picked up.",
        "required": true
      },
      {
        "name": "Estimated Delivery Date",
        "type": "Date",
        "description": "The expected date of delivery.",
        "required": true
      },
      {
        "name": "Actual Delivery Date",
        "type": "Date",
        "description": "The actual date when the parcel was delivered.",
        "required": false
      },
      {
        "name": "Courier Name/ID",
        "type": "String",
        "description": "The name or ID of the courier handling the delivery.",
        "required": true
      },
      {
        "name": "Tracking Number",
        "type": "String",
        "description": "A number used for tracking the parcel's status.",
        "required": true
      },
      {
        "name": "Shipping Cost (USD)",
        "type": "Float",
        "description": "The cost of shipping the parcel in USD.",
        "required": true
      },
      {
        "name": "Insurance Amount (USD)",
        "type": "Float",
        "description": "The amount covered by insurance for the parcel, if applicable.",
        "required": false
      },
      {
        "name": "Parcel Type",
        "type": "String",
        "description": "The type of item being shipped (e.g., documents, electronics, perishable goods).",
        "required": true
      },
      {
        "name": "Special Handling",
        "type": "String",
        "description": "Any special handling instructions (e.g., fragile, temperature-controlled).",
        "required": false
      },
      {
        "name": "Barcode",
        "type": "String",
        "description": "Barcode representation for scanning purposes.",
        "required": true
      },
      {
        "name": "Delivery Signature Required",
        "type": "Boolean",
        "description": "Indicates if the receiver's signature is needed.",
        "required": true
      },
      {
        "name": "Customs Declaration",
        "type": "String",
        "description": "Details for customs if applicable (e.g., item description, value, country of origin).",
        "required": false
      }
    ]
  }
}
