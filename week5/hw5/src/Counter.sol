// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract ECDSA {
    struct ECPoint {
	uint256 x;
	uint256 y;
   }  

    uint256 public constant BASE_FIELD_MODULUS =
        21888242871839275222246405745257275088696311157297823662689037894645226208583;

    uint256 public constant SCALAR_FIELD_MODULUS =
        21888242871839275222246405745257275088548364400416034343698204186575808495617;

    ECPoint public G = ECPoint(1, 2);

    function ecAdd(uint x1, uint y1, uint x2, uint y2) public view returns (uint x3, uint y3) {
        bytes memory payload = abi.encode(x1, y1, x2, y2);
        (bool ok, bytes memory answer) = address(6).staticcall(payload);
        require(ok, "ecAdd Failed");
        (x3, y3) = abi.decode(answer, (uint, uint));
    }

    

function rationalAdd(ECPoint calldata A, ECPoint calldata B, uint256 num, uint256 den) public view returns (bool verified) {
	// return true if the prover knows two numbers that add up to num/den

    
}

}