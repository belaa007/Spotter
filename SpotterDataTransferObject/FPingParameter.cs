using System;
using System.Collections.Generic;
using System.Runtime.Serialization;

namespace SpotterDataTransferObject
{
    /// <summary>
    /// Class for requesting an FPing.
    /// </summary>
    [DataContract]
    public class FPingParameter
    {
        /// <summary>
        /// Gets or sets the IP list.
        /// </summary>
        /// <value>
        /// The IP list.
        /// </value>
        [DataMember]
        public IList<String> IpList { get; set; }
    }
}