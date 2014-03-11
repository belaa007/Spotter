using System;
using System.Runtime.Serialization;

namespace SpotterDataTransferObject
{
    /// <summary>
    /// Class for requesting a Ping.
    /// </summary>
    [DataContract]
    public class PingParameter
    {
        /// <summary>
        /// Gets or sets the Ip.
        /// </summary>
        /// <value>
        /// The Ip.
        /// </value>
        [DataMember]
        public String Ip { get; set; }   
    }
}