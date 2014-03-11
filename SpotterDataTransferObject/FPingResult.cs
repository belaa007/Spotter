using System;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.Serialization;
using SpotterDataTransferObject.PythonComm;

namespace SpotterDataTransferObject
{
    /// <summary>
    /// Class for transfering the FPing result.
    /// </summary>
    [DataContract]
    public class FPingResult
    {
        /// <summary>
        /// Gets or sets the reply.
        /// </summary>
        /// <value>
        /// The reply.
        /// </value>
        [DataMember]
        public FPingReply Reply { get; set; }

        /// <summary>
        /// Gets or sets the nodes.
        /// </summary>
        /// <value>
        /// The nodes.
        /// </value>
        [DataMember]
        public Node[] Nodes { get; set; }
    }
}