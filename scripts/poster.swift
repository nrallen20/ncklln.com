// poster <video> <out.png>: the exact first frame, for a <video poster>
import AVFoundation
import AppKit
let args = CommandLine.arguments
let gen = AVAssetImageGenerator(asset: AVURLAsset(url: URL(fileURLWithPath: args[1])))
gen.appliesPreferredTrackTransform = true
gen.requestedTimeToleranceBefore = .zero
gen.requestedTimeToleranceAfter = .zero
let cg = try gen.copyCGImage(at: .zero, actualTime: nil)
let rep = NSBitmapImageRep(cgImage: cg)
try rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: args[2]))
print("frame \(cg.width)x\(cg.height)")
